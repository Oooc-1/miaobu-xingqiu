from django.db import models
from django.utils import timezone

class Feedback(models.Model):
    # 完美匹配你 feedback.html 里的下拉菜单选项
    TYPE_CHOICES = [
        ('bug', 'BUG反馈（抓个虫）'),
        ('suggest', '功能建议（添块砖）'),
        ('error', '路线纠错（迷路啦）'),
        ('other', '其他想说的话'),
    ]
    
    feedback_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="信件类型")
    nickname = models.CharField(max_length=50, verbose_name="喵友昵称")
    email = models.EmailField(verbose_name="回信邮箱")
    content = models.TextField(verbose_name="信件内容")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="投递时间")
    is_processed = models.BooleanField(default=False, verbose_name="喵喵是否处理/回复")

    class Meta:
        verbose_name = "喵喵信箱"
        verbose_name_plural = "喵喵信箱"
        ordering = ['-created_at'] # 最新的信件排在后台最前面

    def __str__(self):
        return f"[{self.get_feedback_type_display()}] {self.nickname} 的来信"