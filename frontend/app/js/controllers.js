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

var find_predicate = function(wh, predicate) {
    for (int i = 0; i < wh.length; i++) {
        if (predicate(wh[i])) return wh[i];
    }
    return null;
};

gameAppControllers.controller('SolveChallengeCtrl', function SolveChallengeCtrl($scope, $profile, $challenges, $submissions, $routeParams, $instances, $fblogin) {
    console.log("Challenge:");
    console.log($routeParams.challengeid);

    $scope.results = [];

    $scope.update_tests = function() {
        $instances.get_results({
            id: $scope.challenge.puzzle_instance.id
        }, function(results) {
            var tests = $scope.challenge.puzzle_instance.tests;
            var test_list = [];
            for (int i = 0; i < tests.length; i++) {
                test_list.add(new function() {
                    var self = this;
                    self.id = tests[i].id;
                    self.input = tests[i].input;
                    self.solved_by_user = find_predicate(results, function(test) {
                        return test.id === self.id && test.user.fbid === $fblogin.userID;
                    });
                    self.solved_by_enemy = find_predicate(results, function(test) {
                        return test.id === self.id && test.user.fbid !== $fblogin.userID;
                    });
                });
            }
            console.log(test_list);
            $scope.tests = test_list;
            console.log(results);
        }, function(response) {
            console.log("fail");
            console.log(response);
        });
    };

    $scope.submit = function(test_id, output) {
        $submissions.create({
            test: test_id,
            puzzle_instance: $scope.challenge.puzzle_instance.id,
            answer: output,
        }, function(result) {
            console.log("win");
            $scope.update_results();
        }, function(response) {
            console.log("fail");
            console.log(response);
        });
        console.log(test_id, output);
    };

    $challenges.retrieve({id : $routeParams.challengeid}, function(challenge) {
            console.log("Succeeded in getting challenge");
            console.log(challenge);
            $scope.challenge = challenge;
            $scope.update_tests();
        }, function(response) {
            console.log("Failed to get challenge");
            console.log(response);
    });
});
