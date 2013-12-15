from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
import facebook

class FBUser(models.Model):
    user = models.OneToOneField(User)
    fbid = models.TextField()
    access_token = models.TextField()

    def friends(self):
        graph = facebook.GraphAPI(self.access_token)
        friends = graph.get_connections("me", "friends")
        # TODO(enkait): HANDLE PAGING
        userlist = []
        for fbuser in friends['data']:
            friend = FBUser.objects.filter(fbid=fbuser['id']).first()
            if friend:
                userlist.append(friend)
        return userlist

    def save(self, *args, **kwargs):
        user, created = User.objects.get_or_create(username=self.fbid)
        self.user = user
        super(FBUser, self).save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
