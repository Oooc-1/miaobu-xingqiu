from django.shortcuts import render
from django.shortcuts import HttpResponse

def city(request):
    html = '<html><body>城市探险</body></html>'
    return HttpResponse(html)

def forest(request):
    html = '<html><body>森林探险</body></html>'
    return HttpResponse(html)

def alley(request):
    html = '<html><body>巷弄巡逻</body></html>'
    return HttpResponse(html)