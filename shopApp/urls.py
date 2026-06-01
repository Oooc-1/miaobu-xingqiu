from django.urls import path
from . import views

app_name = 'shopApp'

urlpatterns = [
    path('activity/', views.activity, name='activity'), # 逗猫棒(活动)
    path('store/', views.store, name='store'),       # 藏宝阁(商店)
]