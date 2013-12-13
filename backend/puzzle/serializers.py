from django.forms import widgets
from rest_framework import serializers
from puzzle.models import Puzzle, Test, PuzzleInstance, Submission
from django.contrib.auth.models import User

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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

