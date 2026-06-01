from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# 注册你的自定义 User 模型
@admin.register(User)
class MyUserAdmin(UserAdmin):
    # 如果你在 User 模型里增加了自定义字段（比如手机号、头像），可以在这里配置显示
    # 目前先使用 Django 默认的 UserAdmin 配置
    pass