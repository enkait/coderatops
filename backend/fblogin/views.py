from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets, mixins
from fblogin.models import FBUser
from fblogin.serializers import FBUserSerializer, TokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
import facebook

# Create your views here.
class FBUserViewSet(viewsets.GenericViewSet):
    permission_classes = (())
    serializer_class = FBUserSerializer
    queryset = FBUser.objects.all()

    def login(self, request):
        serializer = FBUserSerializer(data=request.DATA)
        serializer.is_valid()

        if serializer.is_valid():
            fbuser, created = FBUser.objects.get_or_create(fbid=serializer.object.fbid)
            fbuser.access_token = serializer.object.access_token
            fbuser.save()

            token = Token.objects.get(user=fbuser.user)
            serialized_token = TokenSerializer(token)

            if created:
                return Response(serialized_token.data, status=status.HTTP_201_CREATED)
            return Response(serialized_token.data, status=status.HTTP_200_OK)
        print "wut"
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

