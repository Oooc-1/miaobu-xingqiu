from django.contrib import admin
from .models import DiaryAlbum, Photo

# 将照片作为相册的“内嵌”部分，这样你在后台添加相册时，就能直接添加照片了
class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1 # 默认显示1个添加照片的空行

@admin.register(DiaryAlbum)
class DiaryAlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    inlines = [PhotoInline] # 启用内嵌功能

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'created_at')
    list_filter = ('album',) # 可以在侧边栏按相册筛选照片