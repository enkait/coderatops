from django.db import models
from django.contrib.auth.models import User

class Puzzle(models.Model):
    title = models.CharField(max_length=200)
    statement = models.CharField(max_length=100000)
    creator = models.ForeignKey(User, related_name="puzzles_created")

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

class Submission(models.Model):
    owner = models.ForeignKey(User, related_name="submissions")
    test = models.ForeignKey(Test, related_name="submissions")
    puzzle_instance = models.ForeignKey(PuzzleInstance, related_name="submissions")
    answer = models.CharField(max_length=1000)

    def ok(self):
        return self.answer == self.test.output
