'use strict';

var gameAppControllers = angular.module('gameAppControllers', ['ngResource', 'fbLoginService']);

gameAppControllers.controller('PuzzleInstanceCtrl', function PuzzleInstanceCtrl($scope, $http, $fbLogin) {
    $http.defaults.useXDomain = true;

    $scope.loginStatus = 'none';
    $scope.isConnected = function() {return $scope.loginStatus === 'connected';};
    $scope.needsLogin = function() {return $scope.loginStatus !== 'none' && $scope.loginStatus !== 'connected';};
    $scope.buttonhtml = function() {return "partials/fbbutton.html";}
    
    var handler = function(response) {
        $scope.$apply(function() {
            $scope.loginStatus = response.status;
        });
    };

    FB.Event.subscribe('auth.authResponseChange', handler);
    FB.getLoginStatus(handler);

    /*
       $http.get('http://localhost:8000/puzzle/puzzles/.json').success(function($data) {
       $scope.puzzles = $data;
       });
       */
});
