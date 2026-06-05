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


class Album(models.Model):
    """个人相册"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums', verbose_name="所属用户")
    title = models.CharField(max_length=100, verbose_name="相册标题")
    description = models.TextField(blank=True, verbose_name="相册描述")
    cover_image = models.ImageField(upload_to='albums/covers/', verbose_name="相册封面", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "个人相册"
        verbose_name_plural = "个人相册"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class Photo(models.Model):
    """相册照片"""
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos', verbose_name="所属相册")
    title = models.CharField(max_length=100, verbose_name="照片标题")
    image = models.ImageField(upload_to='albums/photos/', verbose_name="照片文件")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")

    class Meta:
        verbose_name = "相册照片"
        verbose_name_plural = "相册照片"
        ordering = ['-created_at']

    def __str__(self):
        return self.title