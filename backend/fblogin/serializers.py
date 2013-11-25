from django.forms import widgets
from rest_framework import serializers
from challenge.models import Challenge
from puzzle.serializers import PuzzleInstanceSerializer
from django.contrib.auth.models import User

class FBUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ('fbid', 'access_token')

