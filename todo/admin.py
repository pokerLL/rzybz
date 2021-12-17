from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(todoUser)
admin.site.register(todoList)
admin.site.register(todoItem)
