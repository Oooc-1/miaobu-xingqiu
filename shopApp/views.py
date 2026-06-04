from django.shortcuts import render
from .models import ActivityCategory, StoreShelf


def activity(request):
    categories = ActivityCategory.objects.prefetch_related('activities').all()
    return render(request, 'activity.html', {
        'active_menu': 'shop',
        'sub_menu': 'activity',
        'categories': categories,
    })


def store(request):
    shelves = StoreShelf.objects.prefetch_related('products').all()
    return render(request, 'store.html', {
        'active_menu': 'shop',
        'sub_menu': 'store',
        'shelves': shelves,
    })

