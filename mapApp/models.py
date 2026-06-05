from django.db import models
from django.conf import settings


class Spot(models.Model):
    # 一级分类
    CATEGORY_CHOICES = (
        ('city', '城市探险'),
        ('alley', '巷弄巡逻'),
        ('forest', '森林探险'),
    )

    # 二级板块（专门用于森林页面的分区）
    SUB_CATEGORY_CHOICES = (
        ('route', '秘境路线'),
        ('camping', '躲猫猫营地'),
    )

    # 基础信息
    name = models.CharField(max_length=100, verbose_name="地点名称")
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, verbose_name="分类")
    sub_category = models.CharField(max_length=10, choices=SUB_CATEGORY_CHOICES,
                                    null=True, blank=True, verbose_name="森林版块")
    slug = models.SlugField(unique=True, verbose_name="URL标识")

    # 地理坐标
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="纬度")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="经度")
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="详细地址")

    # 展示内容
    image = models.ImageField(upload_to='spots/', verbose_name="地点图片")
    description = models.TextField(verbose_name="地点简介")
    mood_tag = models.CharField(max_length=50, null=True, blank=True, verbose_name="心情标签")

    # 特色字段
    meow_rate = models.IntegerField(default=0, verbose_name="猫咪出没率(%)")
    cost_desc = models.CharField(max_length=50, null=True, blank=True, verbose_name="费用说明")
    time_required = models.CharField(max_length=50, null=True, blank=True, verbose_name="建议耗时")

    # 统计字段
    view_count = models.IntegerField(default=0, verbose_name="浏览量")
    collect_count = models.IntegerField(default=0, verbose_name="收藏数")

    # 运营控制
    is_featured = models.BooleanField(default=False, verbose_name="是否首页推荐")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "探险地点"
        verbose_name_plural = "探险地点"

    def __str__(self):
        return f"{self.name} ({self.get_category_display()} - {self.sub_category or '无'})"


class SpotCollection(models.Model):
    """景点收藏"""
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name='collections')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('spot', 'user')
        verbose_name = "景点收藏"
        verbose_name_plural = "景点收藏"