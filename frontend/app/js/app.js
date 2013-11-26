'use strict';

var gameApp = angular.module('gameApp', ['ngResource', 'ngCookies', 'gameAppControllers', 'loginService', 'ngRoute', 'ng', 'gameAppDirectives']);

gameApp.run(function ($http, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
});

gameApp.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];
}
]);

gameApp.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when("/login/", {
        templateUrl: 'partials/login.html',
    }).when("/wait/", {
        templateUrl: 'partials/wait.html',
    }).when("/", {
        templateUrl: 'partials/instance.html',
        controller: 'PuzzleInstanceCtrl',
    });
}]);

gameApp.run(function($rootScope, $fbLogin, $location) {
    /*
    $rootScope.$on('$locationChangeStart', function(event, next, current) {
        console.log("locationChangeStart");
        console.log(next);
        console.log(current);
    });
    */
    $rootScope.$on('$routeChangeStart', function(event, next, current) {
        console.log("routing: " + next.route);
        console.log(next);
        console.log($fbLogin.isEstablished());
        if (!$fbLogin.isEstablished()) {
            console.log("rerouting to wait");
            $location.path('/wait/');
        } else {
            if ($fbLogin.isConnected()) {
                console.log("rerouting to main");
                $location.path('/');
            } else {
                console.log("rerouting to login");
                $location.path('/login/');
            }
        }
    });
});
