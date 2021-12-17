from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.chatUser)
admin.site.register(models.chatMessage)