from django.shortcuts import render

def origin(request):
    return render(request,'origin.html',{'active_menu':'about','sub_menu':'origin'})

def team(request):
    return render(request,'team.html',{'active_menu':'about','sub_menu':'team'})