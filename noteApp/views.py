from django.shortcuts import render

def guide(request):
    return render(request, 'guide.html', {'active_menu': 'note', 'sub_menu': 'guide'} )

def food(request):
    return render(request, 'food.html', {'active_menu': 'note', 'sub_menu': 'food'} )

def stay(request):
    return render(request, 'stay.html', {'active_menu': 'note', 'sub_menu': 'stay'} )