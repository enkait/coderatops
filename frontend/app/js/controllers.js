'use strict';

var gameAppControllers = angular.module('gameAppControllers', ['ngResource', 'loginService']);

gameAppControllers.controller('PuzzleInstanceCtrl', function PuzzleInstanceCtrl($scope, $http, $fbLogin, $cookies) {
    $http.defaults.headers.common['Authorization'] = "Token "+$cookies.authToken;
    console.log("Token "+$cookies.authToken);
    $http.get('http://localhost:8000/puzzle/puzzles/.json').success(
        function($data) { $scope.puzzles = $data; });
});
