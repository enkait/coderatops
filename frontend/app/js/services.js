'use strict';

var loginService = angular.module('loginService', ['backendProvider']);

loginService.factory('$fbLogin', function($timeout, $location, $backendAuth, $cookies, $rootScope) {
    return new function() {
        var self = this;

        self.loginStatus = 'none';
        self.authToken = null;
        self.redirect_path = '/';

        self.set_redirect_path = function(path) {
            self.redirect_path = path;
        };

        self.handler = function(response) {
            self.loginStatus = response.status;
            if (self.isConnected()) {
                self.connectedHandler(response);
            } else {
                self.disconnectedHandler(response);
            }
            $timeout(function() {
                console.log("redirecting to", self.redirect_path);
                $location.path(self.redirect_path);
            });
            //self.runHandlers();
        };

        self.runHandlers = function() {
            var newhandlers = [];
            for (var i = 0; i < self.handlers.length; i++) {
                if (self.handlers[i][0]()) {
                    self.handlers[i][1]();
                } else {
                    newhandlers.push(self.handlers[i]);
                }
            }
            self.handlers = newhandlers;
        };

        self.isEstablished = function() {
            return self.loginStatus !== 'none';
        };

        self.isConnected = function() {
            return self.loginStatus === 'connected';
        };

        self.isAuthenticated = function() {
            return self.authToken !== null;
        };

        self.needsLogin = function() {
            return self.loginStatus !== 'none' && $scope.loginStatus !== 'connected';
        };

        self.userID = null;
        self.accessToken = null;

        self.connectedHandler = function(response) {
            self.userID = response.authResponse.userID;
            self.accessToken = response.authResponse.accessToken;
            $backendAuth.login({
                "fbid": self.userID, "access_token": self.accessToken,
            }, function(value, response) {
                self.authToken = value.key
                $cookies.authToken = self.authToken;
                $timeout(function() {
                    console.log("redirecting to", self.redirect_path);
                    $location.path(self.redirect_path);
                });
            }, function(response) {
                console.log(response);
                console.log("fail");
            });
        };

        self.disconnectedHandler = function(response) {
            self.userID = null;
            self.accessToken = null;
            self.authToken = null;
            $cookies.authToken = null;
        };

        self.handlers = [];

        self.registerHandler = function(condition, handler) {
            if (condition()) {
                handler();
            } else {
                self.handlers.push([condition, handler]);
            }
        };

        FB.Event.subscribe('auth.authResponseChange', self.handler);
        FB.getLoginStatus(self.handler);
    };
});

loginService.factory('$backendAuth', function($resource, $backend) {
    return $resource($backend + '/fblogin/fblogin/', [], {
        login: {
            method: 'POST',
            params: {},
            isArray: false,
        },
    });
});

var userDataService = angular.module('userDataService', ['backendProvider']);

userDataService.factory('$friends', function($resource, $cookies, $backend) {
    return $resource($backend + '/fblogin/profile/friends/', [], {
        friends: {
            method: 'GET',
            params: {},
            isArray: true,
            headers: { 'Authorization' : "Token " + $cookies.authToken },
        },
    });
});

userDataService.factory('$challenges', function($resource, $cookies, $fbLogin, $profile, $timeout, $backend) {
    return new function() {
        var self = this;

        self.challenges_api = $resource($backend + '/challenge/challenges/:id', [], {
            create: {
                method: 'POST',
            params: {},
            headers: { 'Authorization' : "Token " + $cookies.authToken },
            },
            list: {
                method: 'GET',
            params: {},
            isArray: true,
            headers: { 'Authorization' : "Token " + $cookies.authToken },
            },
            retrieve: {
                method: 'GET',
            params: {},
            headers: { 'Authorization' : "Token " + $cookies.authToken },
            },
        });

        self.wrap_challenge = function(challenge, success_callback) {
            var Wrapper = function(on_success) {
                var self = this;

                self.id = challenge.id;
                self.challenger = challenge.challenger;
                self.challenged = challenge.challenged;
                if ($fbLogin.userID === self.challenger.fbid) {
                    self.enemy = self.challenged;
                } else {
                    self.enemy = self.challenger;
                }
                self.is_complete = function() {
                    return self.challenger_details && self.challenged_details;
                };
                $profile.get_details(self.challenger.fbid).then(function(details) {
                    self.challenger_details = details;
                    if (self.enemy === self.challenger) {
                        self.enemy_details = details;
                    }
                    if (self.is_complete()) {
                        on_success();
                    }
                });
                $profile.get_details(self.challenged.fbid).then(function(details) {
                    self.challenged_details = details;
                    if (self.enemy === self.challenged) {
                        self.enemy_details = details;
                    }
                    if (self.is_complete()) {
                        on_success();
                    }
                });
                self.message = challenge.message;
                self.puzzle_instance = challenge.puzzle_instance;
            };
            var wrapper = new Wrapper(function() {
                success_callback(wrapper);
            });
        };

        self.wrap_challenge_list = function(challenge_list, success_callback) {
            var wrapped_challenge_list = [];
            if (challenge_list.length === 0) { //will never call append_cb otherwise
                success_callback(wrapped_challenge_list);
                return;
            }
            var append_cb = function(obj) {
                wrapped_challenge_list.push(obj);
                if (wrapped_challenge_list.length === challenge_list.length) {
                    success_callback(wrapped_challenge_list);
                }
            };
            var wrapped_results = challenge_list.map(function(obj) {
                return self.wrap_challenge(obj, append_cb);
            });
        };

        self.create = function(args, success, failure) {
            return self.challenges_api.create(args, function(result) {
                self.wrap_challenge(result, success);
            }, failure);
        };

        self.retrieve = function(args, success, failure) {
            return self.challenges_api.retrieve(args, function(result) {
                self.wrap_challenge(result, success);
            }, failure);
        };

        self.list = function(args, success, failure) {
            return self.challenges_api.list(args, function(result) {
                return self.wrap_challenge_list(result, success);
            }, failure);
        };
    };
});

userDataService.factory('$instances', function($resource, $cookies, $backend) {
    return $resource($backend + '/puzzle/instances/:id', [], {
        get_results: {
            method: 'GET',
           params: {},
           isArray: true,
           headers: { 'Authorization' : "Token " + $cookies.authToken },
        },
        });
});

userDataService.factory('$submissions', function($resource, $cookies, $backend) {
    return $resource($backend + '/puzzle/submissions/', [], {
        create: {
            method: 'POST',
           params: {},
           headers: { 'Authorization' : "Token " + $cookies.authToken },
        },
        });
});

var backendProvider = angular.module('backendProvider', []);

backendProvider.factory('$backend', function($location) {
    return 'http://' + $location.host() + ':8000';
});

backendProvider.factory('$ws', function($location, $cookies) {
    return 'ws://' + $location.host() + ':6379/ws/' + $cookies.authToken;
});

var profileService = angular.module('profileService', ['userDataService']);

// todo: find a good place to put helper functions to avoid duplication
var find_predicate = function(wh, predicate) {
    for (var i = 0; i < wh.length; i++) {
        if (predicate(wh[i])) return wh[i];
    }
    return null;
};

profileService.factory('$profile', function($location, $friends, $q) {
    return new function() {
        var self = this;

        self.profile = function() {
            var d = $q.defer();

            FB.api('/me', {fields: 'name, picture'}, function(response) {
                d.resolve(response);
            });

            return d.promise;
        };

        self.connected_friends = function() {
            var d = $q.defer();

            FB.api('/me/friends', {fields: 'name, picture'}, function(response) {
                $friends.friends({}, function(conn_friends) {
                    var indices = conn_friends.map(function(friend) {
                        return friend.fbid;
                    });
                    var friends = response.data.filter(function(element) {
                        return indices.indexOf(element.id) != -1;
                    });
                    d.resolve(friends);
                });
            });

            return d.promise;
        };

        self.get_details = function(fbid) {
            var d = $q.defer();

            // todo: cache
            self.connected_friends().then(function(friends) {
                var details = find_predicate(friends, function(friend) {
                    return friend.id == fbid;
                });
                if (details) {
                    d.resolve(details);
                    return;
                }
                self.profile().then(function(profile) {
                    if (profile.id === fbid) {
                        d.resolve(profile);
                        return;
                    }
                    d.reject("no such fbid known");
                });
            });

            return d.promise;
        };
    };
});

var messageService = angular.module('messageService', ['backendProvider', 'userDataService']);

messageService.factory('$pubsub', function($ws, $challenges) {
    // TODO: don't constantly create new connections
    return new function() {
        var self = this;

        self.socket = new WebSocket($ws);

        self.handlers = [];

        self.sub = function(handler) {
            console.log("Subscribe");
            self.handlers.push(handler);
        };

        self.unsub = function(handler) {
            console.log("Unsubscribe");
            var pos = self.handlers.indexOf(handler);
            if (pos >= -1) {
                self.handlers.splice(pos, 1);
            } else {
                console.log("No such handler");
            }
        };

        self.socket.onopen = function() {
            console.log("Opened yay");
            self.socket.send("wut");
        };

        self.socket.onerror = function(e) {
            console.log("Error", e);
        };

        self.socket.onmessage = function(e) {
            var obj = JSON.parse(e.data);
            $challenges.wrap_challenge_list(obj.payload, function(wrapped_challenge_list) {
                obj.payload = wrapped_challenge_list;
                console.log("Received", obj);
                for (var i = 0; i < self.handlers.length; i++) {
                    self.handlers[i](obj);
                }
            });
        };

        self.socket.onclose = function(e) {
            console.log("Closed", e);
        };
    };
});
