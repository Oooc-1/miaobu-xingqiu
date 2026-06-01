from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# 注册你的自定义 User 模型
@admin.register(User)
class MyUserAdmin(UserAdmin):
    # fieldsets 决定了在“修改用户”界面显示哪些东西
    # 在原有基础上增加 avatar 和 role
    fieldsets = UserAdmin.fieldsets + (
        ('喵步自定义扩展', {'fields': ('avatar', 'role')}),
    )
    # list_display 决定了在“用户列表”页显示哪些列
    list_display = ('username', 'email', 'role', 'avatar')