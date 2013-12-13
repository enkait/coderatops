from rest_framework.permissions import IsAuthenticated
from puzzle.models import Puzzle, Test, PuzzleInstance, Submission
from django.contrib.auth.models import User
from puzzle.serializers import PuzzleSerializer
from puzzle.serializers import UserSerializer
from puzzle.serializers import TestSerializer
from puzzle.serializers import PuzzleInstanceSerializer
from puzzle.serializers import SubmissionSerializer
from rest_framework import generics
from rest_framework import viewsets
from django.http import Http404
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.decorators import action, link
from rest_framework.response import Response
from puzzle_instance import PuzzleInstanceRatingSerializer
from puzzle_instance import PuzzleInstanceRating
from permissions import IsOwner

class PuzzleViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = ((IsAuthenticated, ))
    serializer_class = PuzzleSerializer
    queryset = Puzzle.objects.all()

    def get_queryset(self):
        print self.request.user
        return Puzzle.objects.filter(creator=self.request.user.pk)

class TestViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = ((IsAuthenticated, ))
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class PuzzleInstanceViewSet(viewsets.ModelViewSet):
    permission_classes = ((IsAuthenticated, ))
    serializer_class = PuzzleInstanceSerializer
    queryset = PuzzleInstance.objects.all()

    @link()
    def rating(self, request, pk, format=None):
        print dir(self.request)
        print request.user
        submissions = Submission.objects.filter(owner=request.user.pk)
        points = len([sub for sub in submissions if sub.ok()])
        rating = PuzzleInstanceRating(points=points)
        serializer = PuzzleInstanceRatingSerializer(rating)
        return Response(serializer.data)

class SubmissionViewSet(viewsets.ModelViewSet):
    permission_classes = ((IsAuthenticated, ))
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()

    def get_queryset(self):
        return Submission.objects.filter(owner=self.request.user.pk)

    def pre_save(self, obj):
        obj.owner = self.request.user

