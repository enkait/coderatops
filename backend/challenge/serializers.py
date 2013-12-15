from django.forms import widgets
from rest_framework import serializers
from challenge.models import Challenge
from puzzle.serializers import PuzzleInstanceSerializer
from django.contrib.auth.models import User

class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ('id', 'challenged', 'message', 'puzzle_instance')

class CreateChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ('challenged', 'message')
