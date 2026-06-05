from django.contrib import admin
from .models import Spot, SpotCollection


@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'meow_rate', 'view_count', 'collect_count', 'is_featured')
    list_filter = ('category', 'is_featured')


@admin.register(SpotCollection)
class SpotCollectionAdmin(admin.ModelAdmin):
    list_display = ('spot', 'user', 'created_at')