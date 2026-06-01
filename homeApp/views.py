from django.shortcuts import render
from noteApp.models import Note  # 从你的 noteApp 导入模型

def home(request):
    # 获取精选游记（is_featured=True），取最新的 3 篇
    featured_notes = Note.objects.filter(is_featured=True).order_by('-created_at')[:3]
    
    return render(request, 'home.html', {
        'active_menu': 'home',
        'featured_notes': featured_notes, # 传递给前端
    })