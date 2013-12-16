from rest_framework.permissions import IsAuthenticated
from challenge.models import Challenge
from django.contrib.auth.models import User
from challenge.serializers import ChallengeSerializer, ChallengeSpecSerializer
from puzzle.models import PuzzleInstance
from fblogin.models import FBUser
from rest_framework import generics
from rest_framework import viewsets
from django.http import Http404
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.decorators import action, link
from rest_framework.response import Response
from rest_framework import status

class ChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = ((IsAuthenticated, ))
    model = Challenge

    def get_queryset(self):
        return Challenge.objects.filter(challenger=self.request.user.pk) | \
            Challenge.objects.filter(challenged=self.request.user.pk)

    def create(self, request):
        serializer = ChallengeSpecSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.object.challenger = request.user
            challenger = request.user
            fbuser = FBUser.objects.filter(fbid=serializer.object.challenged)
            challenged = fbuser.first().user
            message = serializer.object.message
            puzzle_instance = PuzzleInstance.create(challenger, challenged, {})
            puzzle_instance.save()
            challenge = Challenge(challenger=challenger, challenged=challenged,
                    message=message, puzzle_instance=puzzle_instance)
            challenge.save()
            result_serializer = ChallengeSerializer(challenge)
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        challenge = Challenge.objects.filter(pk=pk).first()
        if (challenge != None and challenge.challenger != request.user
                and challenge.challenged != request.user):
            return Response("Can't access this challenge", status=status.HTTP_400_BAD_REQUEST)
        result_serializer = ChallengeSerializer(challenge)
        return Response(result_serializer.data, status=status.HTTP_200_OK)
