from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save

class FBUser(models.Model):
    fbid = models.TextField(primary_key=True)
    user = models.OneToOneField(User)
    access_token = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        user, created = User.objects.get_or_create(username=self.fbid)
        self.user = user
        super(FBUser, self).save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
