from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('my-nest/', views.my_nest, name='my_nest'),
    path('change-avatar/', views.change_avatar, name='change_avatar'),
    # 相册相关
    path('my-albums/', views.my_albums, name='my_albums'),
    path('create-album/', views.create_album, name='create_album'),
    path('album/<int:album_id>/', views.album_detail, name='album_detail'),
    path('album/<int:album_id>/upload-photo/', views.upload_photo, name='upload_photo'),
    # 好友系统
    path('friends/', views.friend_list, name='friend_list'),
    path('search-users/', views.search_users, name='search_users'),
    path('friend/send/', views.send_friend_request, name='send_friend_request'),
    path('friend/accept/', views.accept_friend_request, name='accept_friend_request'),
    path('friend/reject/', views.reject_friend_request, name='reject_friend_request'),
    # 私聊
    path('chat/<int:friend_id>/', views.chat_room, name='chat_room'),
    path('chat/<int:friend_id>/history/', views.chat_history, name='chat_history'),
    path('chat/send/', views.send_message, name='send_message'),
    path('chat/poll/', views.poll_messages, name='poll_messages'),
    # 通知
    path('notifications/', views.notification_list, name='notification_list'),
    path('unread-count/', views.unread_count, name='unread_count'),
    path('mark-read/', views.mark_read, name='mark_read'),
]