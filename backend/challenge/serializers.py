from django.forms import widgets
from rest_framework import serializers
from challenge.models import Challenge
from puzzle.serializers import PuzzleInstanceSerializer
from django.contrib.auth.models import User

class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ('id', 'challenged', 'title', 'puzzle_instance')

class ChallengeSpec(object):
    def __init__(self, puzzle_instance_serializer, challenge_serializer):
        self.puzzle_instance_serializer = puzzle_instance_serializer
        self.challenge_serializer = challenge_serializer

class ChallengeSpecSerializer(serializers.Serializer):
    puzzle_instance = PuzzleInstanceSerializer
    challenge = ChallengeSerializer

    def restore_object(self, attrs, instance=None):
        if instance:
            raise Exception("Can't modify existing object")
        print attrs.keys()
        return ChallengeSpec(**attrs)
