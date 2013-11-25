'use strict';

var gameApp = angular.module('gameApp', ['ngResource', 'ngCookies', 'gameAppControllers', 'fbLoginService', 'ngRoute', 'ng', 'gameAppDirectives']);

gameApp.run(function ($http, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
});

gameApp.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];
}
]);

gameApp.config(['$routeProvider', function($routeProvider) {
    $routeProvider.otherwise({
        templateUrl: 'partials/instance.html',
        controller: 'PuzzleInstanceCtrl',
    });
}]);
