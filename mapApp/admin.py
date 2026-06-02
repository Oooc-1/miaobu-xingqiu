from django.contrib import admin
from .models import Spot

@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'meow_rate', 'is_featured')
    list_filter = ('category', 'is_featured')