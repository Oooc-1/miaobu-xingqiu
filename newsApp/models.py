from django.db import models

# 1. 定义相册模型
class DiaryAlbum(models.Model):
    title = models.CharField(max_length=100, verbose_name="相册名称")
    cover_image = models.ImageField(upload_to='diary/covers/', verbose_name="相册封面")
    description = models.TextField(blank=True, verbose_name="相册简介")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "追光日记相册"
        verbose_name_plural = "追光日记相册"

# 2. 定义照片模型
class Photo(models.Model):
    # 下面这一整块请确保每个字段名前面都有 4 个空格
    album = models.ForeignKey(DiaryAlbum, on_delete=models.CASCADE, related_name='photos', verbose_name="所属相册")
    title = models.CharField(max_length=100, verbose_name="照片标题")
    image = models.ImageField(upload_to='diary/photos/', verbose_name="日记照片")
    
    # 这些是可选字段，确保缩进也是 4 个空格
    latitude = models.CharField(max_length=20, verbose_name="纬度", blank=True, null=True)
    longitude = models.CharField(max_length=20, verbose_name="经度", blank=True, null=True)
    shutter_speed = models.CharField(max_length=20, verbose_name="快门速度", blank=True, null=True)
    aperture = models.CharField(max_length=20, verbose_name="光圈", blank=True, null=True)
    iso = models.IntegerField(verbose_name="ISO感光度", blank=True, null=True)
    
    # 这一行就是报错的那一行，请特别注意它前面的空格必须和上面的字段完全对齐
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "拍立得照片"
        verbose_name_plural = "拍立得照片"