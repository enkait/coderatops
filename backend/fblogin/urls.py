from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import viewsets, routers
from fblogin.views import FBUserViewSet, ProfileViewSet
from puzzle.models import Puzzle
from django.contrib.auth.models import User

class FBLoginRouter(routers.DefaultRouter):
    routes = [
        routers.Route(url=r'^{prefix}$',
            mapping={'post': 'login'},
            name='login',
            initkwargs={}),
    ]

fb_login_router = FBLoginRouter()
fb_login_router.register(r'fblogin', FBUserViewSet)

class ProfileRouter(routers.DefaultRouter):
    routes = [
        routers.Route(url=r'^{prefix}/friends$',
            mapping={'get': 'list'},
            name='friends-list',
            initkwargs={}),
    ]

profile_router = ProfileRouter()
profile_router.register(r'profile', ProfileViewSet)

urlpatterns = patterns(
    'fblogin.views',
    url(r'^', include(fb_login_router.urls)),
    url(r'^', include(profile_router.urls)),
)
