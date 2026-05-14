from django.shortcuts import render
from django.shortcuts import HttpResponse

def origin(request):
    html = '<html><body>星球起源</body></html>'
    return HttpResponse(html)

def team(request):
    html = '<html><body>喵喵团队</body></html>'
    return HttpResponse(html)