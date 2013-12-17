from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import viewsets, routers
from puzzle import views
from puzzle.views import PuzzleViewSet
from puzzle.views import TestViewSet, PuzzleInstanceViewSet, SubmissionViewSet
from puzzle.models import Puzzle

class SubmissionRouter(routers.DefaultRouter):
    routes = [
        routers.Route(url=r'^{prefix}$',
            mapping={'post': 'create'},
            name='create',
            initkwargs={}),
    ]

submission_router = SubmissionRouter()
submission_router.register(r'submissions', SubmissionViewSet)

class PuzzleInstanceRouter(routers.DefaultRouter):
    routes = [
        routers.Route(url=r'^{prefix}/{lookup}$',
            mapping={'get': 'results'},
            name='results',
            initkwargs={}),
    ]

puzzle_instance_router = PuzzleInstanceRouter()
puzzle_instance_router.register(r'instances', PuzzleInstanceViewSet)

router = routers.DefaultRouter()
router.register(r'puzzles', PuzzleViewSet)
router.register(r'tests', TestViewSet)

urlpatterns = patterns('puzzle.views',
    url(r'^', include(router.urls)),
    url(r'^', include(submission_router.urls)),
    url(r'^', include(puzzle_instance_router.urls)),
)
