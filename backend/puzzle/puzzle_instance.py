from django.db import models
from django.forms import widgets
from rest_framework import serializers
from puzzle.models import Puzzle, Test, PuzzleInstance, Submission

class PuzzleInstanceRating:
    def __init__(self, points=None):
        self.points = points

class PuzzleInstanceRatingSerializer(serializers.Serializer):
    points = serializers.IntegerField()

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.points = attrs.get('points', instance.points)
            return instance
        return PuzzleInstanceRating(**attrs)
