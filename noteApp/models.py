from django.db import models
from django.conf import settings

# 1. 游记主表
class Note(models.Model):
    # 分类选择
    NOTE_CATEGORIES = (
        (1, '旅行踩点指南'),
        (2, '出行干粮补给'),
        (3, '躲雨小窝推荐'),
    )
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="作者")
    title = models.CharField(max_length=200, verbose_name="标题")
    summary = models.CharField(max_length=500, verbose_name="摘要")
    content = models.TextField(verbose_name="正文内容")
    cover_image = models.ImageField(upload_to='notes/covers/', verbose_name="封面图", blank=True, null=True)
    category = models.IntegerField(choices=NOTE_CATEGORIES, default=1, verbose_name="分类")
    is_featured = models.BooleanField(default=False, verbose_name="是否首页精选")
    
    # 统计字段（使用空间换时间，提高读取性能）
    view_count = models.IntegerField(default=0, verbose_name="浏览量")
    like_count = models.IntegerField(default=0, verbose_name="点赞数")
    collect_count = models.IntegerField(default=0, verbose_name="收藏数")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "游记"
        ordering = ['-created_at']

# 2. 评论表
class NoteComment(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='comments', verbose_name="所属游记")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="评论者")
    content = models.TextField(verbose_name="评论内容")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies', verbose_name="父级评论")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    class Meta:
        verbose_name = "游记评论"
        verbose_name_plural = "游记评论"

# 3. 点赞表
class NoteLike(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('note', 'user')  # 关键点：防止重复点赞
        verbose_name = "游记点赞"
        verbose_name_plural = "游记点赞"

# 4. 收藏表
class NoteCollection(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='collections')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('note', 'user')  # 关键点：防止重复收藏
        verbose_name = "游记收藏"
        verbose_name_plural = "游记收藏"