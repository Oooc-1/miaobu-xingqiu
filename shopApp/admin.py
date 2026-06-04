from django.contrib import admin
from .models import ActivityCategory, ActivityItem, StoreShelf, StoreProduct

@admin.register(ActivityCategory)
class ActivityCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ActivityItem)
class ActivityItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location')

@admin.register(StoreShelf)
class StoreShelfAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')

@admin.register(StoreProduct)
class StoreProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'shelf', 'price')