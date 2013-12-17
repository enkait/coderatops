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
    $profile.connected_friends().then(function(friends) {
        $scope.friends = friends;
    });

    $scope.challenge = function(friend, message) {
        message = message || "";
        $challenges.create({
            challenged: friend.id,
            message: message,
        }, function(challenge) {
            $location.path('/challenge/' + challenge.id);
        }, function(response) {
            console.log("fail");
            console.log(response);
        });
    };
});

gameAppControllers.controller('SolveChallengeCtrl', function SolveChallengeCtrl($scope, $profile, $challenges, $submissions, $routeParams, $instances, $fbLogin, $timeout) {
    var find_predicate = function(wh, predicate) {
        for (var i = 0; i < wh.length; i++) {
            if (predicate(wh[i])) return wh[i];
        }
        return null;
    };

    $scope.results = [];

    $scope.update_tests = function() {
        $instances.get_results({
            id: $scope.challenge.puzzle_instance.id
        }, function(results) {
            var tests = $scope.challenge.puzzle_instance.tests;
            var test_list = [];
            for (var i = 0; i < tests.length; i++) {
                test_list.push(new function() {
                    var self = this;
                    self.id = tests[i].id;
                    self.input = tests[i].input;
                    var enemy = $scope.challenge.enemy;
                    self.solved_by_user = null !== find_predicate(results, function(test) {
                        return test.test.id === self.id && test.user.fbid === $fbLogin.userID && test.result > 0;
                    });
                    self.solved_by_enemy = null !== find_predicate(results, function(test) {
                        return test.test.id === self.id && test.user.fbid === enemy && test.result > 0;
                    });
                    self.attempted_by_user = null !== find_predicate(results, function(test) {
                        return test.test.id === self.id && test.user.fbid === $fbLogin.userID;
                    });
                    self.attempted_by_enemy = null !== find_predicate(results, function(test) {
                        return test.test.id === self.id && test.user.fbid === enemy;
                    });
                });
            }
            if (!$scope.tests) {
                $scope.tests = test_list;
            } else {
                for (var i = 0; i < test_list.length; i++) {
                    $scope.tests[i].solved_by_user = test_list[i].solved_by_user;
                    $scope.tests[i].solved_by_enemy = test_list[i].solved_by_enemy;
                    $scope.tests[i].attempted_by_user = test_list[i].attempted_by_user;
                    $scope.tests[i].attempted_by_enemy = test_list[i].attempted_by_enemy;
                }
            }
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
            $scope.update_tests();
        }, function(response) {
            console.log("fail");
            console.log(response);
        });
    };

    $challenges.retrieve({id : $routeParams.challengeid}, function(challenge) {
        $scope.challenge = challenge;
        $scope.update_tests();
        $scope.test_updater = function() {
            $scope.update_tests();
            $scope.current_timeout_promise = $timeout($scope.test_updater, 2000);
        };
        $scope.current_timeout_promise = $timeout($scope.test_updater, 2000);
        $scope.$on('$destroy', function(){
            $timeout.cancel($scope.current_timeout_promise);
        });
    }, function(response) {
        console.log("Failed to get challenge");
        console.log(response);
    });
});
