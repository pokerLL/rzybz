from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import *


# Register your models here.


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'idd', 'nickname', 'account', 'c_time', 'email', 'has_confirmed', ]
    list_filter = ['is_vaild', 'has_confirmed']
    # fields = [ 'nickname', 'account', ('is_vaild', 'has_confirmed')]
    actions_on_top = True
    # list_display_links = ['id', 'idd', 'nickname']

    # actions_on_bottom = True
    # save_on_top = True
    search_fields = ['nickname', 'email']

    def idd(self, obj):
        return obj.id

    idd.short_description = "ID"


@admin.register(ConfirmStatus)
class ConfirmStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'c_time')
