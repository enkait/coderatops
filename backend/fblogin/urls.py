from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import viewsets, routers
from fblogin.views import FBUserViewSet
from puzzle.models import Puzzle
from django.contrib.auth.models import User

router = routers.DefaultRouter()
router.register(r'fblogin', FBUserViewSet)

urlpatterns = patterns('fblogin.views',
    url(r'^', include(router.urls)),
)
