'use strict';

var gameApp = angular.module('gameApp', ['ngResource', 'ngCookies']);

gameApp.run(function ($http, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
});
