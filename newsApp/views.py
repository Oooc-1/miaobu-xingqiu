from django.shortcuts import render
from django.shortcuts import HttpResponse

def news(request):
    html = '<html><body>今日鱼干</body></html>'
    return HttpResponse(html)

def diary(request):
    html = '<html><body>追光日记</body></html>'
    return HttpResponse(html)