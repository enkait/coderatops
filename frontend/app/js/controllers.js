var gameApp = angular.module('gameApp', ['ngResource']);

gameApp.controller('PuzzleInstanceCtrl', function PuzzleInstanceCtrl($scope) {
    /*
    if (!('query' in $scope)) {
        $scope.query = 'omg';
    }
    */
    $scope.puzzles = [
    {
        'title' : 'n po k',
        'content' : '3 po 12',
    },
    {
        'title' : 'n po k2',
        'content' : '8 po 4',
    }
    ];
});
