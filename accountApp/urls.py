from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-nest/', views.my_nest, name='my_nest'),
    path('change-avatar/', views.change_avatar, name='change_avatar'),
    # 相册相关
    path('my-albums/', views.my_albums, name='my_albums'),
    path('create-album/', views.create_album, name='create_album'),
    path('album/<int:album_id>/', views.album_detail, name='album_detail'),
    path('album/<int:album_id>/upload-photo/', views.upload_photo, name='upload_photo'),
]