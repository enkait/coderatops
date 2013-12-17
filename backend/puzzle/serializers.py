from django.forms import widgets
from rest_framework import serializers
from puzzle.models import Puzzle, Test, PuzzleInstance, Submission
from fblogin.models import FBUser

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('id', 'puzzle', 'input', 'difficulty')

class SmallTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('id',)

class PuzzleSerializer(serializers.ModelSerializer):
    tests = TestSerializer(many=True)
    class Meta:
        model = Puzzle
        fields = ('id', 'title', 'statement', 'tests')

class PuzzleInstanceSerializer(serializers.ModelSerializer):
    tests = TestSerializer(many=True)
    class Meta:
        model = PuzzleInstance
        fields = ('id', 'puzzle', 'tests')

class SubmissionSerializer(serializers.ModelSerializer):
    #test = TestSerializer() - doesn't allow submit
    class Meta:
        model = Submission
        fields = ('id', 'test', 'puzzle_instance', 'answer')

class FBUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBUser
        fields = ('fbid',)

class TestResult(object):
    def __init__(self, test, result, user):
        self.test = test
        self.result = result
        self.user = user

class ResultSerializer(serializers.Serializer):
    test = SmallTestSerializer()
    result = serializers.IntegerField()
    user = FBUserSerializer()
