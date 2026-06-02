from django.shortcuts import render
from .models import DiaryAlbum, Photo, NewsCategory

def news(request):
    categories = NewsCategory.objects.prefetch_related('items').order_by('title')
    return render(request, 'news.html', {
        'active_menu': 'news',
        'sub_menu': 'news-item',
        'categories': categories,
    })

def diary(request):
    photos = Photo.objects.select_related('album').order_by('-created_at')[:9]
    return render(request, 'diary.html', {
        'active_menu': 'news',
        'sub_menu': 'diary-item',
        'photos': photos,
    })

