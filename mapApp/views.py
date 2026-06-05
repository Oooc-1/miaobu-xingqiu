from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .models import Spot, SpotCollection


def city(request):
    selected_mood = request.GET.get('mood', 'all')
    spots = Spot.objects.filter(category='city')
    if selected_mood and selected_mood != 'all':
        spots = spots.filter(mood_tag__icontains=selected_mood)
    spots = spots.order_by('-is_featured', '-created_at')
    return render(request, 'city.html', {
        'active_menu': 'map',
        'sub_menu': 'city',
        'spots': spots,
        'selected_mood': selected_mood,
    })


def forest(request):
    # 分别查询秘境路线和躲猫猫营地
    routes = Spot.objects.filter(category='forest', sub_category='route').order_by('-is_featured', '-created_at')
    camps = Spot.objects.filter(category='forest', sub_category='camping').order_by('-is_featured', '-created_at')
    
    return render(request, 'forest.html', {
        'routes': routes,
        'camps': camps,
        'active_menu': 'map', 
        'sub_menu': 'forest'
    })

def alley(request):
    selected_mood = request.GET.get('mood', 'all')
    spots = Spot.objects.filter(category='alley')
    if selected_mood and selected_mood != 'all':
        spots = spots.filter(mood_tag__icontains=selected_mood)
    spots = spots.order_by('-is_featured', '-created_at')
    return render(request, 'alley.html', {
        'active_menu': 'map',
        'sub_menu': 'alley',
        'spots': spots,
        'selected_mood': selected_mood,
    })


def spot_detail(request, slug):
    spot = get_object_or_404(Spot, slug=slug)
    # 原子自增浏览量
    Spot.objects.filter(id=spot.id).update(view_count=F('view_count') + 1)
    spot.refresh_from_db()
    return render(request, 'spot_detail.html', {'active_menu': 'map', 'spot': spot})


@login_required
def collect_spot(request, slug):
    spot = get_object_or_404(Spot, slug=slug)
    collection, created = SpotCollection.objects.get_or_create(spot=spot, user=request.user)
    if created:
        spot.collect_count += 1
        spot.save()
        status = 'collected'
    else:
        collection.delete()
        spot.collect_count -= 1
        spot.save()
        status = 'uncollected'
    return JsonResponse({'status': status, 'count': spot.collect_count})

