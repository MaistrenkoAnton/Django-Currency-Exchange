from django.contrib import admin
from .models import Rate


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):

    list_display = ('currency', 'value', 'updated')
