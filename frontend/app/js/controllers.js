var gameApp = angular.module('gameApp', ['ngResource'])

gameApp.controller('PuzzleInstanceCtrl', function PuzzleInstanceCtrl($scope) {
    $scope.puzzle = {
        'title' : 'n po k',
    }
});
