from django.contrib import admin
from .models import SocialUser

class AdminSocialUser(admin.ModelAdmin):
    pass

admin.site.register(SocialUser, AdminSocialUser)
