from django.contrib import admin

from .models import Gamer


@admin.register(Gamer)
class GamerAdmin(admin.ModelAdmin):
    pass
