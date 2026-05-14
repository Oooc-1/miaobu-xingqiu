from django.shortcuts import render
from django.shortcuts import HttpResponse

def cooperate(request):
    html = '<html><body>蹭蹭求抱</body></html>'
    return HttpResponse(html)

def feedback(request):
    html = '<html><body>喵喵信箱</body></html>'
    return HttpResponse(html)