from django.contrib import admin
from .models import Profile
# Register your models here.


class AdminProfile(admin.ModelAdmin):
    list_display = ['user','date_of_birth','photo']

admin.site.register(Profile,AdminProfile)
