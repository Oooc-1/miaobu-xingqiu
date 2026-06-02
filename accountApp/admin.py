from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# 注册你的自定义 User 模型
@admin.register(User)
class MyUserAdmin(UserAdmin):
    
    fieldsets = UserAdmin.fieldsets + (
        ('个人信息', {'fields': ('avatar',)}),
    )
    # 或者在 list_display 中添加，以便在列表页看到
    list_display = ('username', 'email', 'avatar')