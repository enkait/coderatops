from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import viewsets, routers
from puzzle import views
from puzzle.views import PuzzleViewSet
from puzzle.views import TestViewSet, PuzzleInstanceViewSet, SubmissionViewSet
from puzzle.models import Puzzle

router = routers.DefaultRouter()
router.register(r'puzzles', PuzzleViewSet)
router.register(r'tests', TestViewSet)
router.register(r'instances', PuzzleInstanceViewSet)
router.register(r'submissions', SubmissionViewSet)

urlpatterns = patterns('puzzle.views',
    url(r'^', include(router.urls)),
)
