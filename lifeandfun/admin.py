from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.lifeUser)
admin.site.register(models.lifeArticle)
admin.site.register(models.lifeComment)
admin.site.register(models.lifeTag)