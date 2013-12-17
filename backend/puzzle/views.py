from rest_framework.permissions import IsAuthenticated
from puzzle.models import Puzzle, Test, PuzzleInstance, Submission
from puzzle.serializers import PuzzleSerializer, FBUserSerializer, TestSerializer, TestResult
from puzzle.serializers import PuzzleInstanceSerializer, SubmissionSerializer, ResultSerializer
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
from fblogin.models import FBUser

class PuzzleViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = ((IsAuthenticated, ))
    serializer_class = PuzzleSerializer
    queryset = Puzzle.objects.all()

    def get_queryset(self):
        return Puzzle.objects.filter(creator=self.request.user.pk)

class TestViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = ((IsAuthenticated, ))
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class PuzzleInstanceViewSet(viewsets.GenericViewSet):
    permission_classes = ((IsAuthenticated, ))
    serializer_class = PuzzleInstanceSerializer
    model = PuzzleInstance

    def rating(self, request, pk, format=None):
        submissions = Submission.objects.filter(owner=request.user.pk)
        points = len([sub for sub in submissions if sub.ok()])
        rating = PuzzleInstanceRating(points=points)
        serializer = PuzzleInstanceRatingSerializer(rating)
        return Response(serializer.data)

    def get_results(self, p_instance, user):
        submissions = Submission.objects.filter(owner=user, puzzle_instance=p_instance)
        results = {}
        for sub in submissions:
            test_result = results.get(sub.test.id, TestResult(sub.test, sub.points(), user))
            if test_result.result < sub.points():
                test_result.result = sub.points()
            results[sub.test.id] = test_result
        return results.values()

    def results(self, request, pk, format=None):
        p_instance = PuzzleInstance.objects.filter(id=pk).first()
        challenge = p_instance.challenge
        results = self.get_results(p_instance, challenge.challenger)
        results += self.get_results(p_instance, challenge.challenged)
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)

class SubmissionViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = ((IsAuthenticated, ))
    serializer_class = SubmissionSerializer
    model = Submission

    # todo: reject submissions if test already solved (or handle in results())

    def get_queryset(self):
        return Submission.objects.filter(owner=self.request.user.pk)

    def pre_save(self, obj):
        obj.owner = FBUser.objects.filter(user=self.request.user).first()
