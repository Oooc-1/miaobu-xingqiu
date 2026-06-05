from django.urls import path
from . import views

app_name = 'noteApp'

urlpatterns = [
    path('guide/', views.guide, name='guide'),
    path('food/', views.food, name='food'),
    path('stay/', views.stay, name='stay'),
    path('create/', views.create_note, name='create_note'),
    path('<int:note_id>/', views.note_detail, name='detail'),
    # 新增交互接口
    path('like/<int:note_id>/', views.like_note, name='like_note'),
    path('comment/<int:note_id>/', views.add_comment, name='add_comment'),
]