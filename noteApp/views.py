from django.shortcuts import render
from django.shortcuts import HttpResponse

def guide(request):
    html = '<html><body>踩点指南</body></html>'
    return HttpResponse(html)

def food(request):
    html = '<html><body>干粮补给</body></html>'
    return HttpResponse(html)

def stay(request):
    html = '<html><body>躲雨小窝</body></html>'
    return HttpResponse(html)