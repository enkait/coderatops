from django.db import models
from fblogin.models import FBUser
import random

class Puzzle(models.Model):
    title = models.CharField(max_length=200)
    statement = models.CharField(max_length=100000)
    creator = models.ForeignKey(FBUser, related_name="puzzles_created")

class Test(models.Model):
    DIFFICULTY_CHOICES = (
        ("easy", "easy"),
        ("medium", "medium"),
        ("hard", "hard"),
    )

    puzzle = models.ForeignKey(Puzzle, related_name="tests")
    input = models.CharField(max_length=1000)
    output = models.CharField(max_length=1000)
    difficulty = models.CharField(max_length=100, choices=DIFFICULTY_CHOICES)

class PuzzleInstance(models.Model):
    puzzle = models.ForeignKey(Puzzle, related_name="puzzle_instances")
    tests = models.ManyToManyField(Test, related_name="puzzle_instances")

    @staticmethod
    def create(challenger, challenged, spec):
        puzzle = random.choice(Puzzle.objects.all())
        instance = PuzzleInstance(puzzle=puzzle)
        instance.save()
        for test in Test.objects.filter(puzzle=puzzle):
            instance.tests.add(test)
        instance.save()
        return instance

class Submission(models.Model):
    owner = models.ForeignKey(FBUser, related_name="submissions")
    test = models.ForeignKey(Test, related_name="submissions")
    puzzle_instance = models.ForeignKey(PuzzleInstance, related_name="submissions")
    answer = models.CharField(max_length=1000)

    def points(self):
        return 1 if self.answer == self.test.output else 0
