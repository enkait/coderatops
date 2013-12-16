from challenge.models import Challenge
from django.contrib import admin

class ChallengeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Challenge, ChallengeAdmin)
