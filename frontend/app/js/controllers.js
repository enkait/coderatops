'use strict';

var gameAppControllers = angular.module('gameAppControllers', ['ngResource', 'loginService', 'profileService']);

gameAppControllers.controller('PuzzleInstanceCtrl', function PuzzleInstanceCtrl($scope, $http, $fbLogin, $cookies, $profile) {
    $http.get('http://localhost:8000/puzzle/puzzles/.json').success(
        function($data) { $scope.puzzles = $data; });
    $profile.connected_friends().then(function(friends) {
        $scope.friends = friends;
    });
});

gameAppControllers.controller('ChallengeCtrl', function ChallengeCtrl($scope, $profile, $challenges, $location) {
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
        }, function(challenge) {
            console.log("success");
            $location.path('/challenge/' + challenge.id);
        }, function(response) {
            console.log("fail");
            console.log(response);
        });
    };
});

gameAppControllers.controller('SolveChallengeCtrl', function SolveChallengeCtrl($scope, $profile, $challenges, $routeParams) {
    console.log("Challenge:");
    console.log($routeParams.challengeid);
    $challenges.retrieve({id : $routeParams.challengeid}, function(challenge) {
            console.log("Succeeded in getting challenge");
            console.log(challenge);
            $scope.challenge = challenge
        }, function(response) {
            console.log("Failed to get challenge");
            console.log(response);
    });
});
