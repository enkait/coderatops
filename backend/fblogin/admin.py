from fblogin.models import FBUser
from django.contrib import admin

class FBUserAdmin(admin.ModelAdmin):
    model = FBUser

admin.site.register(FBUser, FBUserAdmin)
