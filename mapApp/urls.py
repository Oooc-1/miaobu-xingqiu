from django.urls import path
from . import views

app_name='mapApp'

urlpatterns=[
    path('city/', views.city, name='city'),                 # 城市探险
    path('forest/', views.forest, name='forest'),           # 森林探险
    path('alley/', views.alley, name='alley'),              # 巷弄巡逻
    path('spot/<slug:slug>/', views.spot_detail, name='spot_detail'),
    path('spot/<slug:slug>/collect/', views.collect_spot, name='collect_spot'),
    path('forest-booking/', views.forest_booking, name='forest_booking'),
]