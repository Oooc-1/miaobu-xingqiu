from django.db import models

# --- 1. 逗猫棒 (活动) 模块 ---

class ActivityCategory(models.Model):
    COLOR_CHOICES = [
        ('#FF9F89', '元气珊瑚粉 (活动特色)'),
        ('#A7C4BC', '清新薄荷绿 (自然/环保)'),
        ('#4A4E69', '沉稳暗夜蓝 (人文/考古)'),
        ('#FFC857', '活力明黄 (探险/任务)'),
        ('#E9C46A', '复古奶咖 (手作/文化)'),
        ('#2A9D8F', '森林深绿 (户外/徒步)'),
        ('#E76F51', '暖阳陶土红 (艺术/民俗)'),
        ('#8D99AE', '静谧灰蓝 (研学/科普)'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="活动类别") # 如：深度限定体验
    badge_color = models.CharField(
        max_length=20, 
        choices=COLOR_CHOICES, # 开启下拉菜单
        default='#FF9F89', 
        verbose_name="标签背景色"
    )
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "活动分类"
        verbose_name_plural = "活动分类"

class ActivityItem(models.Model):
    category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE, related_name="activities", verbose_name="所属分类")
    title = models.CharField(max_length=200, verbose_name="活动名称")
    cover_image = models.ImageField(upload_to='activity/', verbose_name="封面图")
    duration = models.CharField(max_length=50, verbose_name="耗时")
    location = models.CharField(max_length=200, verbose_name="地点")
    description = models.TextField(verbose_name="活动简介")
    services = models.CharField(max_length=500, verbose_name="活动包含(用逗号隔开)")
    booking_link = models.URLField(verbose_name="预订链接")
    
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "特色活动"
        verbose_name_plural = "特色活动"

# --- 2. 藏宝阁 (商店) 模块 ---

class StoreShelf(models.Model):
    title = models.CharField(max_length=100, verbose_name="货架名称") # 如：第一层：喵步原创文创
    order = models.IntegerField(default=0, verbose_name="排序权重")
    
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['order']
        verbose_name = "货架分类"
        verbose_name_plural = "货架分类"

class StoreProduct(models.Model):
    shelf = models.ForeignKey(StoreShelf, on_delete=models.CASCADE, related_name="products", verbose_name="所属货架")
    name = models.CharField(max_length=200, verbose_name="商品名称")
    image = models.ImageField(upload_to='store/', verbose_name="商品图")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    description = models.TextField(verbose_name="商品简介")
    purchase_guide = models.TextField(blank=True, verbose_name="购买指南/备注") # 存放保质期、鉴别方法等
    link = models.URLField(verbose_name="购买链接")
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "周边商品"
        verbose_name_plural = "周边商品"