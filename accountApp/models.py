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


class Friendship(models.Model):
    """好友关系"""
    STATUS_CHOICES = (
        ('pending', '待确认'),
        ('accepted', '已添加'),
        ('rejected', '已拒绝'),
    )
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_received')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')
        verbose_name = "好友关系"
        verbose_name_plural = "好友关系"


class PrivateMessage(models.Model):
    """私聊消息"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_received')
    content = models.TextField(verbose_name="消息内容")
    is_read = models.BooleanField(default=False, verbose_name="已读")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "私聊消息"
        verbose_name_plural = "私聊消息"
        ordering = ['created_at']


class Notification(models.Model):
    """通知"""
    NTYPE_CHOICES = (
        ('friend_request', '好友申请'),
        ('friend_accepted', '好友通过'),
        ('mention', '@提及'),
        ('like', '点赞'),
        ('comment', '评论'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name="接收者")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_sent', verbose_name="触发者")
    ntype = models.CharField(max_length=20, choices=NTYPE_CHOICES, verbose_name="通知类型")
    content = models.CharField(max_length=500, verbose_name="通知内容")
    related_url = models.CharField(max_length=300, blank=True, verbose_name="跳转链接")
    is_read = models.BooleanField(default=False, verbose_name="已读")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "通知"
        verbose_name_plural = "通知"
        ordering = ['-created_at']