'use strict';

var fbLoginService = angular.module('fbLoginService', []);

fbLoginService.factory('$fbLogin', function($window) {
    return new function() {
        this.logged_in = false;
        this.online = false;

        this.handler = function(response) {
            this.online = true;
            if (response.status === 'connected') {
                this.logged_in = true;
                console.log('connected');
            } else if (response.status === 'not_authorized') {
                this.logged_in = false;
                console.log('not_authorized');
            } else {
                this.logged_in = false;
                console.log('unknown');
            }
        };

        this.is_logged_in = function() {
            return this.logged_in;
        };

        this.is_online = function() {
            return this.online;
        };

        FB.Event.subscribe('auth.authResponseChange', this.handler);
        FB.getLoginStatus(this.handler);
    };
});
