'use strict';

var loginService = angular.module('loginService', []);

loginService.factory('$fbLogin', function($window, $timeout, $location, $backendAuth, $cookies) {
    return new function() {
        var self = this;

        self.loginStatus = 'none';
        self.authToken = null;

        self.handler = function(response) {
            self.loginStatus = response.status;
            console.log("handler fblogin");
            console.log(self.loginStatus);
            if (self.isConnected()) {
                self.connectedHandler(response);
            } else {
                self.disconnectedHandler(response);
            }
            $timeout(function() {$location.path('/');});
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
                $timeout(function() {$location.path('/');});
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

loginService.factory('$backendAuth', function($window, $timeout, $location, $resource) {
    return $resource('http://localhost:8000/fblogin/fblogin/', [], {
        login: {
            method: 'POST',
            params: {},
            isArray: false,
        },
    });
});

var userDataService = angular.module('userDataService', []);

userDataService.factory('$friends', function($window, $timeout, $location, $resource) {
    return $resource('http://localhost:8000/fblogin/profile/friends/', [], {
        friends: {
            method: 'GET',
            params: {},
            isArray: true,
        },
    });
});

var profileService = angular.module('profileService', ['userDataService']);

profileService.factory('$profile', function($window, $timeout, $location, $resource, $friends, $q) {
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
