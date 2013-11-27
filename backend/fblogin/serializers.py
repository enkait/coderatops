from django.forms import widgets
from rest_framework import serializers
from fblogin.models import FBUser
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class FBUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBUser
        fields = ('fbid', 'access_token')

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)
