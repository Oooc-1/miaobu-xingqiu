from django.shortcuts import render

def city(request):
    return render(request, 'city.html',{'active_menu':'map','sub_menu':'city'})

def forest(request):
    return render(request, 'forest.html',{'active_menu':'map','sub_menu':'forest'})

def alley(request):
    return render(request, 'alley.html',{'active_menu':'map','sub_menu':'alley'})
