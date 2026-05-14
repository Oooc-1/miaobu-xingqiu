from django.urls import path
from . import views

app_name='aboutApp'

urlpatterns=[
    path('origin/', views.origin, name='origin'),    # 星球起源
    path('team/', views.team, name='team'),          # 喵喵团队
]