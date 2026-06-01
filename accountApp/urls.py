from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-nest/', views.my_nest, name='my_nest'),
    path('change-avatar/', views.change_avatar, name='change_avatar'),
]