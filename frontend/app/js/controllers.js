var gameApp = angular.module('gameApp', ['ngResource']);

gameApp.controller('PuzzleInstanceCtrl', function PuzzleInstanceCtrl($scope, $http) {
    $http.defaults.useXDomain = true;

    $http.get('http://localhost:8000/puzzle/puzzles/.json').success(function(data) {
        $scope.puzzles = $data;
    });
});
