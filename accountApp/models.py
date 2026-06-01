from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # 将 default 指向你的默认头像路径（相对于 MEDIA_ROOT）
    avatar = models.ImageField(
        upload_to='avatar/', 
        blank=True, 
        null=True, 
        default='avatar/default_cat_avatar.jpg'  # 这里添加默认值
    )
    # 也可以顺便把你的“用户角色分析”里的角色加上（选填，方便后续分权）
    ROLE_CHOICES = (
        ('visitor', '普通游客'),
        ('user', '注册喵友'),
        ('admin', '博主/管理员'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    class Meta:
        db_table = 'accountApp_user'  # 保持好看的表名