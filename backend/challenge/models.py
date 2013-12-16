from django.db import models
from fblogin.models import FBUser
from puzzle.models import Puzzle, Test, PuzzleInstance, Submission

class Challenge(models.Model):
    challenger = models.ForeignKey(FBUser, related_name="challenges_posed")
    challenged = models.ForeignKey(FBUser, related_name="challenges_received")
    message = models.CharField(max_length=200)
    puzzle_instance = models.ForeignKey(PuzzleInstance, related_name="challenges")
