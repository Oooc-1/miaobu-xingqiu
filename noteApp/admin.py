from django.contrib import admin
from .models import Note, NoteComment, NoteLike, NoteCollection, CommentLike

# 1. 评论内联（方便在游记详情页直接看到评论）
class CommentInline(admin.TabularInline):
    model = NoteComment
    extra = 0  # 默认不显示空的评论条目
    readonly_fields = ('created_at',)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_featured', 'like_count', 'collect_count', 'created_at')
    list_filter = ('category', 'is_featured', 'created_at')
    search_fields = ('title', 'author__username')
    inlines = [CommentInline]  # 这一行让后台管理游记时能直接看到评论

@admin.register(NoteComment)
class NoteCommentAdmin(admin.ModelAdmin):
    list_display = ('note', 'user', 'content', 'created_at')
    search_fields = ('content', 'user__username', 'note__title')
    list_filter = ('created_at',)

# 2. 注册点赞和收藏（使用自定义显示方便查看）
@admin.register(NoteLike)
class NoteLikeAdmin(admin.ModelAdmin):
    list_display = ('note', 'user', 'created_at')
    list_filter = ('created_at',)

@admin.register(NoteCollection)
class NoteCollectionAdmin(admin.ModelAdmin):
    list_display = ('note', 'user', 'created_at')

# 3. 注册新增的评论点赞
@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user', 'created_at')