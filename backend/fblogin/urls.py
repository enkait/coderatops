from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import viewsets, routers
from fblogin.views import FBUserViewSet
from puzzle.models import Puzzle
from django.contrib.auth.models import User

class FBLoginRouter(routers.DefaultRouter):
    routes = [
        routers.Route(url=r'^{prefix}/login$',
            mapping={'post': 'login'},
            name='login',
            initkwargs={}),
    ]

router = FBLoginRouter()
router.register(r'fblogin', FBUserViewSet)

urlpatterns = patterns( 'fblogin.views', url(r'^', include(router.urls)), )
