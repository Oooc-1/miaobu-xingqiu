from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    自定义用户模型
    """
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)
    
    ROLE_CHOICES = (
        ('visitor', '普通游客'),
        ('user', '注册喵友'),
        ('admin', '博主/管理员'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    class Meta:
        db_table = 'accountApp_user'

    def __str__(self):
        return self.username