var gameApp = angular.module('gameApp', ['ngResource']);

gameApp.controller('PuzzleInstanceCtrl', function PuzzleInstanceCtrl($scope) {
    $scope.puzzles = [
    {
        'title' : 'n po k',
    },
    {
        'title' : 'n po k2',
    }
    ]
});
