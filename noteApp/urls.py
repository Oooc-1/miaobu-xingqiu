from django.urls import path
from . import views

app_name='noteApp'

urlpatterns=[
    path('guide/', views.guide, name='guide'),       # 踩点指南
    path('food/', views.food, name='food'),          # 干粮补给
    path('stay/', views.stay, name='stay'),          # 躲雨小窝
]