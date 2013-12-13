from django.forms import widgets
from rest_framework import serializers
from fblogin.models import FBUser
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import facebook

class FBUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBUser
        fields = ('fbid', 'access_token')

    def validate(self, attrs):
        graph = facebook.GraphAPI(attrs['access_token'])
        profile = graph.get_object("me")
        if profile['id'] != attrs['fbid']:
            raise serializers.ValidationError("access token does not match fbid")
        return attrs

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)
