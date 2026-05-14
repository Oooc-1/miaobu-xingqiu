from django.shortcuts import render
from django.shortcuts import HttpResponse

def activity(request):
    html = '<html><body>逗猫棒</body></html>'
    return HttpResponse(html)

def store(request):
    html = '<html><body>藏宝阁</body></html>'
    return HttpResponse(html)
