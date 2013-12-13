from rest_framework.permissions import IsAuthenticated
from challenge.models import Challenge
from django.contrib.auth.models import User
from challenge.serializers import ChallengeSerializer, ChallengeSpecSerializer
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
    serializer_class = ChallengeSerializer
    queryset = Challenge.objects.all()

    def get_queryset(self):
        return Challenge.objects.filter(challenger=self.request.user.pk) | \
            Challenge.objects.filter(challenged=self.request.user.pk)

    def create(self, request):
        serializer = ChallengeSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.object.challenger = request.user
            serializer.save()
            """
            serializer.puzzle_instance.save()
            serializer.challenge.challenger = request.user
            serializer.challenge.save()
            """
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
