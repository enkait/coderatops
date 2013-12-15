'use strict';

var gameApp = angular.module('gameApp', ['ngResource', 'ngCookies', 'gameAppControllers', 'loginService', 'ngRoute', 'ng', 'gameAppDirectives']);

gameApp.run(function ($http, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
});

gameApp.config(['$httpProvider', function($httpProvider) {
    //$httpProvider.defaults.useXDomain = true;
    //delete $httpProvider.defaults.headers.common['X-Requested-With'];
}
]);

gameApp.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when("/login/", {
        templateUrl: 'partials/login.html',
    }).when("/wait/", {
        templateUrl: 'partials/wait.html',
    }).when("/challenge/", {
        templateUrl: 'partials/challenge.html',
    }).when("/", {
        templateUrl: 'partials/instance.html',
        controller: 'PuzzleInstanceCtrl',
    });
}]);

var update_true_path = function($rootScope, cur_path) {
    console.log("updating");
    console.log(cur_path);
    console.log($rootScope.true_path);
};

gameApp.run(function($rootScope, $fbLogin, $location) {
    $rootScope.$on('$routeChangeStart', function(event, next, current) {
        var cur_path = $location.path();
        if (cur_path !== '/wait/' && cur_path !== '/login/') {
            $fbLogin.set_redirect_path(cur_path);
        }
        if (!$fbLogin.isEstablished()) {
            $location.path('/wait/');
        } else if (!$fbLogin.isConnected()) {
            $location.path('/login/');
        } else if (!$fbLogin.isAuthenticated()) {
            $location.path('/wait/');
        } else {
            console.log("NOT REROUTING");
        }
    });
});
