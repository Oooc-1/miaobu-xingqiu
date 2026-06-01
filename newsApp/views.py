from django.shortcuts import render

def news(request):
    return render(request, 'news.html', {'active_menu': 'news', 'sub_menu': 'news-item'})

def diary(request):
    return render(request, 'diary.html', {'active_menu': 'news', 'sub_menu': 'diary-item'})

