from django.forms import widgets
from rest_framework import serializers
from challenge.models import Challenge
from puzzle.serializers import PuzzleInstanceSerializer
from django.contrib.auth.models import User

class ChallengeSerializer(serializers.ModelSerializer):
    challenged = serializers.CharField(max_length=200)
    challenger = serializers.CharField(max_length=200)

    class Meta:
        model = Challenge
        fields = ('id', 'challenger', 'challenged', 'message', 'puzzle_instance')

class ChallengeSpec(object):
    def __init__(self, challenged, message):
        self.challenged = challenged
        self.message = message

class ChallengeSpecSerializer(serializers.Serializer):
    challenged = serializers.CharField(max_length=200)
    message = serializers.CharField(max_length=200, required=False)

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.challenged = attrs.get('challenged', instance.challenged)
            instance.message = attrs.get('message', instance.message)
            return instance
        return ChallengeSpec(**attrs)
