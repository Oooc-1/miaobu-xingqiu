from django.shortcuts import render

def activity(request):
    return render(request, 'activity.html',{'active_menu':'shop','sub_menu':'activity'})

def store(request):
    return render(request, 'store.html',{'active_menu':'shop','sub_menu':'store'})

