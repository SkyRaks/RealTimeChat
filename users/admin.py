# from django.contrib import admin
# from .models import Profile
#
# # Register your models here.
# admin.site.register(Profile)

from django.contrib import admin
from .models import Profile
from rtchat.models import ChatGroup, GroupMessage

admin.site.register(Profile)
admin.site.register(ChatGroup)
admin.site.register(GroupMessage)
