'use strict';

var gameAppControllers = angular.module('gameAppControllers', ['ngResource', 'fbLoginService']);

gameAppControllers.controller('PuzzleInstanceCtrl', function PuzzleInstanceCtrl($scope, $http, $fbLogin) {
    $http.defaults.useXDomain = true;
    alert(FB.getLoginStatus());

    $http.get('http://localhost:8000/puzzle/puzzles/.json').success(function($data) {
        $scope.puzzles = $data;
    });
});
