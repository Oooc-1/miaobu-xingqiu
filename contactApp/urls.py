from django.urls import path
from . import views

app_name='contactApp'

urlpatterns=[
    path('cooperate/', views.cooperate, name='cooperate'),    # 蹭蹭求抱(商务合作)
    path('feedback/', views.feedback, name='feedback'),       # 喵喵信箱(反馈)
]