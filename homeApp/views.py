from django.shortcuts import render
from noteApp.models import Note  # 从你的 noteApp 导入模型
from mapApp.models import Spot

def home(request):
    # 获取精选游记（is_featured=True），取最新的 3 篇
    featured_notes = Note.objects.filter(is_featured=True).order_by('-created_at')[:3]
    # 获取首页推荐的目的地（mapApp Spot.is_featured=True），取最新的 6 个
    featured_spots = Spot.objects.filter(is_featured=True).order_by('-created_at')[:6]

    return render(request, 'home.html', {
        'active_menu': 'home',
        'featured_notes': featured_notes, # 传递给前端
        'featured_spots': featured_spots,
    })