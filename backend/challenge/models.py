from django.db import models
from django.contrib.auth.models import User
from puzzle.models import Puzzle, Test, PuzzleInstance, Submission

class Challenge(models.Model):
    challenger = models.ForeignKey(User, related_name="challenges_posed")
    challenged = models.ForeignKey(User, related_name="challenges_received")
    message = models.CharField(max_length=200, blank=True)
    puzzle_instance = models.ForeignKey(PuzzleInstance, related_name="challenges")
