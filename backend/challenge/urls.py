from django.conf.urls.defaults import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import viewsets, routers
from challenge import views
from challenge.views import ChallengeViewSet
from puzzle.models import Puzzle
from django.contrib.auth.models import User

router = routers.DefaultRouter()
router.register(r'challenges', ChallengeViewSet)

urlpatterns = patterns('challenge.views',
    url(r'^', include(router.urls)),
)
