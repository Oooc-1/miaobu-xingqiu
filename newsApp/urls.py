from django.urls import path
from . import views

app_name='newsApp'

urlpatterns=[
    path('news/', views.news, name='news'),             # 今日鱼干
    path('diary/', views.diary, name='diary'),          # 追光日记
]