from django.forms import widgets
from rest_framework import serializers
from puzzle.models import Puzzle, Test, PuzzleInstance, Submission
from fblogin.models import FBUser

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('id', 'puzzle', 'input', 'difficulty')

class PuzzleSerializer(serializers.ModelSerializer):
    tests = TestSerializer(many=True)
    class Meta:
        model = Puzzle
        fields = ('id', 'title', 'statement', 'tests')

class PuzzleInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuzzleInstance
        fields = ('id', 'puzzle', 'tests')

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'test', 'puzzle_instance', 'answer')

class FBUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBUser
        fields = ('id', 'username')

