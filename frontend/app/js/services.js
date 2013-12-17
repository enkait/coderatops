'use strict';

var loginService = angular.module('loginService', []);

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
            console.log("handler fblogin");
            console.log(self.loginStatus);
            if (self.isConnected()) {
                self.connectedHandler(response);
            } else {
                self.disconnectedHandler(response);
            }
            $timeout(function() {
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
                console.log("success");
                console.log(self.authToken);
                $timeout(function() {
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

loginService.factory('$backendAuth', function($resource) {
    return $resource('http://localhost:8000/fblogin/fblogin/', [], {
        login: {
            method: 'POST',
            params: {},
            isArray: false,
        },
    });
});

var userDataService = angular.module('userDataService', []);

userDataService.factory('$friends', function($resource, $cookies) {
    return $resource('http://localhost:8000/fblogin/profile/friends/', [], {
        friends: {
            method: 'GET',
            params: {},
            isArray: true,
            headers: { 'Authorization' : "Token " + $cookies.authToken },
        },
    });
});

userDataService.factory('$challenges', function($resource, $cookies, $fbLogin) {
    return new function() {
        var self = this;

        self.challenges_api = $resource('http://localhost:8000/challenge/challenges/:id', [], {
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

        self.wrap_challenge = function(challenge) {
            return new function() {
                var self = this;

                self.id = challenge.id;
                self.challenger = challenge.challenger;
                self.challenged = challenge.challenged;
                self.message = challenge.message;
                self.puzzle_instance = challenge.puzzle_instance;

                if ($fbLogin.userID === self.challenger.fbid) {
                    self.enemy = self.challenged.fbid;
                } else {
                    self.enemy = self.challenger.fbid;
                }
            };
        };

        self.create = function(args, success, failure) {
            console.log(self);
            return self.challenges_api.create(args, function(result) {
                console.log(self);
                return success(self.wrap_challenge(result));
            }, failure);
        };

        self.retrieve = function(args, success, failure) {
            console.log(self);
            return self.challenges_api.retrieve(args, function(result) {
                console.log(self);
                return success(self.wrap_challenge(result));
            }, failure);
        };
    };
});

userDataService.factory('$instances', function($resource, $cookies) {
    return $resource('http://localhost:8000/puzzle/instances/:id', [], {
        get_results: {
            method: 'GET',
           params: {},
           isArray: true,
           headers: { 'Authorization' : "Token " + $cookies.authToken },
        },
        });
});

userDataService.factory('$submissions', function($resource, $cookies) {
    return $resource('http://localhost:8000/puzzle/submissions/', [], {
        create: {
            method: 'POST',
           params: {},
           headers: { 'Authorization' : "Token " + $cookies.authToken },
        },
        });
});

var profileService = angular.module('profileService', ['userDataService']);

profileService.factory('$profile', function($location, $friends, $q) {
    return new function() {
        var self = this;

        self.connected_friends = function() {
            var d = $q.defer();

            FB.api('/me/friends', {fields: 'name'}, function(response) {
                $friends.friends({}, function(conn_friends) {
                    var indices = conn_friends.map(function(friend) {
                        console.log(friend);
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
    };
});
