from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets, mixins
from fblogin.models import FBUser
from fblogin.serializers import FBUserSerializer, TokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.
class FBUserViewSet(viewsets.GenericViewSet):
    permission_classes = (())
    serializer_class = FBUserSerializer
    queryset = FBUser.objects.all()

    def login(self, request):
        serializer = FBUserSerializer(data=request.DATA)
        print "OK"
        print serializer.object
        serializer.is_valid()
        print serializer.errors
        # TODO: VERIFY!!!!!!
        # FOR NOW WE PRETTY MUCH TAKE THEIR WORD FOR IT

        if serializer.is_valid():
            print "omg"
            fbuser, created = FBUser.objects.get_or_create(fbid=serializer.object.fbid)
            fbuser.access_token = serializer.object.access_token
            fbuser.save()

            token = Token.objects.get(user=fbuser.user)
            print token
            serialized_token = TokenSerializer(token)
            print serialized_token
            if created:
                return Response(serialized_token.data, status=status.HTTP_201_CREATED)
            return Response(serialized_token.data, status=status.HTTP_200_OK)
        print "wut"
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

