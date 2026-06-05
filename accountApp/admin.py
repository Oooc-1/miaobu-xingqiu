from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Album, Photo


# 注册你的自定义 User 模型
@admin.register(User)
class MyUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        ('个人信息', {'fields': ('avatar',)}),
    )
    # 或者在 list_display 中添加，以便在列表页看到
    list_display = ('username', 'email', 'avatar')


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    list_filter = ('user',)
    search_fields = ('title', 'user__username')
    inlines = [PhotoInline]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'created_at')
    list_filter = ('album',)