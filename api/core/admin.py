from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    ...


admin.site.register(Post, PostAdmin)
