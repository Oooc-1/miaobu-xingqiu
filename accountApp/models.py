from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    自定义用户模型，继承自带的 AbstractUser
    直接塞入头像字段，告别双表关联的繁琐！
    """
    # 头像字段，允许为空，上传后存在 media/avatar/ 目录下
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)
    
    # 也可以顺便把你的“用户角色分析”里的角色加上（选填，方便后续分权）
    ROLE_CHOICES = (
        ('visitor', '普通游客'),
        ('user', '注册喵友'),
        ('admin', '博主/管理员'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    class Meta:
        db_table = 'accountApp_user'  # 保持好看的表名