'use strict';

var gameApp = angular.module('gameApp', ['ngResource', 'ngCookies', 'gameAppControllers', 'fbLoginService']);

gameApp.run(function ($http, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
});

gameApp.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];
}
]);
