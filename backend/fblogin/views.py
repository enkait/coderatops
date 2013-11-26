from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets, mixins
from fblogin.models import FBUser
from fblogin.serializers import FBUserSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status

# Create your views here.
class FBUserViewSet(viewsets.ViewSet):
    permission_classes = (())
    serializer_class = FBUserSerializer
    queryset = FBUser.objects.all()

    def login(self, request):
        serializer = FBUserSerializer(data=request.DATA)
        # TODO: VERIFY!!!!!!
        # FOR NOW WE PRETTY MUCH TAKE THEIR WORD FOR IT
        if serializer.is_valid():
            fbuser, created = FBUser.objects.get_or_create(fbid=serializer.fbid)
            fbuser.access_token = serializer.access_token

            token = Token.objects.get(user=fbuser.user)
            if created:
                return Response(token, status=status.HTTP_201_CREATED)
            return Response(token, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

