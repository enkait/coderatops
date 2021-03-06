'use strict';

var gameAppDirectives = angular.module("gameAppDirectives", []);

gameAppDirectives.directive("fbMarkup", function($rootScope) {
    return function (scope, iElement, iAttrs) {
        FB.XFBML.parse(iElement[0]);
    };
});

gameAppDirectives.directive("navbar", function() {
    return {
        templateUrl: "partials/navbar.html",
    }; 
});
