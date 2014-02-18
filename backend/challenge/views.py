from rest_framework.permissions import IsAuthenticated
from challenge.models import Challenge
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
from rest_framework.authtoken.models import Token
import traceback
from pubsub.pubsub import pub_sub_finder

class ChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = ((IsAuthenticated, ))
    model = Challenge

    def get_queryset(self):
        fbuser = FBUser.objects.get(user=self.request.user)
        return Challenge.objects.filter(challenger=fbuser).order_by('pk') | \
            Challenge.objects.filter(challenged=fbuser).order_by('pk')

    def create(self, request):
        serializer = ChallengeSpecSerializer(data=request.DATA)
        if serializer.is_valid():
            try:
                serializer.object.challenger = request.user
                challenger = FBUser.objects.filter(user=request.user).first()
                fbuser = FBUser.objects.filter(fbid=serializer.object.challenged)
                challenged = fbuser.first()
                message = serializer.object.message
                puzzle_instance = PuzzleInstance.create(challenger, challenged, {})
                challenge = Challenge(challenger=challenger, challenged=challenged,
                        message=message, puzzle_instance=puzzle_instance)
                challenge.save()
                result_serializer = ChallengeSerializer(challenge)
                self.publish_list(request.user)
            except Exception as ex:
                traceback.print_exc()
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        challenge = Challenge.objects.filter(pk=pk).first()
        fbuser = FBUser.objects.filter(user=request.user).first()
        if (challenge != None and challenge.challenger != fbuser
                and challenge.challenged != fbuser):
            return Response("Can't access this challenge", status=status.HTTP_400_BAD_REQUEST)
        result_serializer = ChallengeSerializer(challenge)
        return Response(result_serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        result_serializer = ChallengeSerializer(self.get_queryset(), many=True)
        print result_serializer.data
        return Response(result_serializer.data, status=status.HTTP_200_OK)

    def publish_list(self, user):
        token = Token.objects.get(user=user)
        result_serializer = ChallengeSerializer(self.get_queryset(), many=True)
        print result_serializer.data
        pub_sub_finder.get(str(token)).pub("challenge_list", result_serializer.data)
