from django.contrib import admin
from .models import Note, NoteComment, NoteLike, NoteCollection

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_featured', 'like_count', 'created_at')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'author__username')

admin.site.register(NoteComment)
admin.site.register(NoteLike)
admin.site.register(NoteCollection)