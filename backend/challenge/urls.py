from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import viewsets, routers
from challenge import views
from challenge.views import ChallengeViewSet

class ChallengeRouter(routers.DefaultRouter):
    routes = [
        routers.Route(url=r'^{prefix}$',
            mapping={'post': 'create'},
            name='create',
            initkwargs={}),
        routers.Route(url=r'^{prefix}/{lookup}$',
            mapping={'get': 'retrieve'},
            name='retrieve',
            initkwargs={}),
    ]

challenge_router = ChallengeRouter()
challenge_router.register(r'challenges', ChallengeViewSet)

urlpatterns = patterns('challenge.views',
    url(r'^', include(challenge_router.urls)),
)
