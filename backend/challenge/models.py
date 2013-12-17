from django.db import models
from fblogin.models import FBUser
from puzzle.models import Puzzle, Test, PuzzleInstance, Submission

class Challenge(models.Model):
    challenger = models.ForeignKey(FBUser, related_name="challenges_posed")
    challenged = models.ForeignKey(FBUser, related_name="challenges_received")
    message = models.CharField(max_length=200)
    puzzle_instance = models.OneToOneField(PuzzleInstance)

    def __unicode__(self):
        return "%s: %s vs %s" % (unicode(self.pk),
                unicode(self.challenger.fbid), unicode(self.challenged.fbid))
