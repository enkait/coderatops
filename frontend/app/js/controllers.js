'use strict';

var gameAppControllers = angular.module('gameAppControllers', ['ngResource', 'loginService', 'profileService']);

gameAppControllers.controller('PuzzleInstanceCtrl', function PuzzleInstanceCtrl($scope, $http, $fbLogin, $cookies, $profile) {
    $http.get('http://localhost:8000/puzzle/puzzles/.json').success(
        function($data) { $scope.puzzles = $data; });
    $profile.connected_friends().then(function(friends) {
        $scope.friends = friends;
    });
});

gameAppControllers.controller('ChallengeCtrl', function ChallengeCtrl($scope, $profile, $challenges) {
    console.log("Challenged:");
    console.log($scope.challenged);
    $profile.connected_friends().then(function(friends) {
        $scope.friends = friends;
    });

    $scope.challenge = function(friend, message) {
        message = message || "";
        console.log(friend);
        console.log(message);
        $challenges.create({
            challenged: friend.id,
            message: message,
        }, function(friend) {
            console.log("success");
        }, function(response) {
            console.log("fail");
            console.log(response);
        });
    };
});
