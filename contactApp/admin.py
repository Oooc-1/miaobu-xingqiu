from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    # 后台列表页展示哪些列
    list_display = ('feedback_type', 'nickname', 'email', 'created_at', 'is_processed')
    # 过滤器：可以按类型和处理状态筛选
    list_filter = ('feedback_type', 'is_processed', 'created_at')
    # 搜索框：可以按昵称、邮箱、内容搜索
    search_fields = ('nickname', 'email', 'content')
    # 列表页可以直接修改是否处理
    list_editable = ('is_processed',)
    
    # 核心魔法：向 Django Admin 页面注入我们的猫咪色板 CSS
    class Media:
        css = {
            'all': ('css/admin_theme.css',) # 我们在下面配置这个专属 CSS 文件
        }

# 修改后台管理系统的顶部大标题和站点标记
admin.site.site_header = "🐾 喵步星球 · 核心中控台"
admin.site.site_title = "喵步星球后台"
admin.site.index_title = "欢迎来到喵步星球管理后台"