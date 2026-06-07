import json
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from .models import Album, Photo, User, Friendship, PrivateMessage, Notification
from noteApp.models import NoteLike, NoteCollection
from mapApp.models import SpotCollection


# 通用登录与身份自动分流
def login_view(request):
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')

        # 检查用户名是否存在
        if not User.objects.filter(username=u).exists():
            return render(request, 'login.html', {
                'error': '喵呜，这个账号还不存在哦！快去注册吧~ 🐾',
                'active_menu': 'home',
                'suggest_register': True,
                'last_username': u
            })

        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            if user.is_superuser or user.is_staff:
                return redirect('admin:index')
            else:
                return redirect('home')
        else:
            return render(request, 'login.html', {
                'error': '喵呜，暗号或密码错啦！🐾',
                'active_menu': 'home'
            })

    return render(request, 'login.html', {'active_menu': 'home'})


# 注册新用户
def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        password2 = request.POST.get('password2', '').strip()

        if not username or not password:
            return render(request, 'register.html', {
                'error': '喵呜，账号和暗号都不能为空哦！🐾',
                'active_menu': 'home'
            })

        if len(username) < 3:
            return render(request, 'register.html', {
                'error': '喵呜，账号至少需要3个字符哦！🐾',
                'active_menu': 'home'
            })

        if password != password2:
            return render(request, 'register.html', {
                'error': '喵呜，两次输入的暗号不一致！🐾',
                'active_menu': 'home'
            })

        if len(password) < 6:
            return render(request, 'register.html', {
                'error': '喵呜，暗号至少需要6个字符哦！🐾',
                'active_menu': 'home'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': '喵呜，这个账号已经被别的铲屎官占用啦！换个名字试试~ 🐾',
                'active_menu': 'home'
            })

        # 创建用户（role 默认 'user'）
        User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'register.html', {'active_menu': 'home'})


# 退出登录
def logout_view(request):
    logout(request)
    return redirect('home')


# 普通用户的个人中心：我的猫巢
@login_required(login_url='login')
def my_nest(request):
    # 获取用户点赞的游记（带游记详情，按点赞时间倒序）
    liked_notes = NoteLike.objects.filter(user=request.user).select_related(
        'note', 'note__author'
    ).order_by('-created_at')

    # 获取用户收藏的游记（带游记详情，按收藏时间倒序）
    collected_notes = NoteCollection.objects.filter(user=request.user).select_related(
        'note', 'note__author'
    ).order_by('-created_at')

    # 获取用户收藏的景点（带景点详情，按收藏时间倒序）
    collected_spots = SpotCollection.objects.filter(user=request.user).select_related(
        'spot'
    ).order_by('-created_at')

    return render(request, 'my_nest.html', {
        'user': request.user,
        'active_menu': 'home',
        'liked_notes': liked_notes,
        'collected_notes': collected_notes,
        'collected_spots': collected_spots,
    })


@login_required(login_url='login')
def change_avatar(request):
    if request.method == "POST":
        action = request.POST.get('action', '')

        # 修改头像
        if action == 'avatar':
            new_avatar = request.FILES.get('avatar_file')
            if new_avatar:
                request.user.avatar = new_avatar
                request.user.save()
                return render(request, 'change_avatar.html', {
                    'success': '喵呜！新头像保存成功啦！✨',
                    'active_menu': 'home'
                })
            else:
                return render(request, 'change_avatar.html', {
                    'error': '你好像还没有选择任何猫片哦？🐾',
                    'active_menu': 'home'
                })

        # 修改昵称
        if action == 'nickname':
            new_nickname = request.POST.get('nickname', '').strip()
            if not new_nickname:
                return render(request, 'change_avatar.html', {
                    'error': '喵呜，昵称不能为空哦！🐾',
                    'active_menu': 'home'
                })
            if len(new_nickname) < 2:
                return render(request, 'change_avatar.html', {
                    'error': '喵呜，昵称至少需要2个字符！🐾',
                    'active_menu': 'home'
                })
            if new_nickname == request.user.username:
                return render(request, 'change_avatar.html', {
                    'error': '喵呜，新昵称和当前昵称一样哦！🐾',
                    'active_menu': 'home'
                })
            # 检查是否被占用
            if User.objects.filter(username=new_nickname).exclude(id=request.user.id).exists():
                return render(request, 'change_avatar.html', {
                    'error': '喵呜，这个昵称已经被别的铲屎官占用啦！🐾',
                    'active_menu': 'home'
                })
            request.user.username = new_nickname
            request.user.save()
            return render(request, 'change_avatar.html', {
                'success': '喵呜！昵称修改成功！「' + new_nickname + '」听起来真棒 ✨',
                'active_menu': 'home'
            })

    return render(request, 'change_avatar.html', {'active_menu': 'home'})


# ==================== 相册相关视图 ====================

@login_required(login_url='login')
def my_albums(request):
    """查看用户的所有相册"""
    albums = request.user.albums.all()
    return render(request, 'my_albums.html', {
        'user': request.user,
        'active_menu': 'home',
        'albums': albums,
    })


@login_required(login_url='login')
def create_album(request):
    """创建新相册"""
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        cover_image = request.FILES.get('cover_image')

        if title:
            album = Album.objects.create(
                user=request.user,
                title=title,
                description=description,
                cover_image=cover_image if cover_image else None
            )
            return redirect('album_detail', album_id=album.id)
        else:
            return render(request, 'create_album.html', {
                'error': '喵呜，相册标题不能为空哦！🐾',
                'active_menu': 'home'
            })

    return render(request, 'create_album.html', {'active_menu': 'home'})


@login_required(login_url='login')
def album_detail(request, album_id):
    """查看相册详情（仅限自己的相册）"""
    album = get_object_or_404(Album, id=album_id, user=request.user)
    photos = album.photos.all()
    return render(request, 'album_detail.html', {
        'album': album,
        'photos': photos,
        'active_menu': 'home'
    })


@login_required(login_url='login')
def upload_photo(request, album_id):
    """上传照片到指定相册"""
    album = get_object_or_404(Album, id=album_id, user=request.user)

    if request.method == "POST":
        title = request.POST.get('title')
        image = request.FILES.get('image')

        if title and image:
            Photo.objects.create(
                album=album,
                title=title,
                image=image
            )
            return redirect('album_detail', album_id=album.id)
        else:
            return render(request, 'upload_photo.html', {
                'album': album,
                'error': '喵呜，照片标题和照片文件都不能为空哦！🐾',
                'active_menu': 'home'
            })

    return render(request, 'upload_photo.html', {
        'album': album,
        'active_menu': 'home'
    })


# ==================== 好友系统 ====================

@login_required(login_url='login')
def friend_list(request):
    """好友列表 + 待处理请求"""
    # 已接受的好友（预计算对方用户对象，避免模板复杂逻辑）
    raw_friends = Friendship.objects.filter(
        Q(from_user=request.user) | Q(to_user=request.user),
        status='accepted'
    ).select_related('from_user', 'to_user')
    friends = []
    for f in raw_friends:
        friends.append({
            'user': f.to_user if f.from_user == request.user else f.from_user,
            'friendship': f,
        })

    # 收到的好友申请
    pending_received = Friendship.objects.filter(
        to_user=request.user, status='pending'
    ).select_related('from_user')

    # 发出的好友申请
    pending_sent = Friendship.objects.filter(
        from_user=request.user, status='pending'
    ).select_related('to_user')

    return render(request, 'friends.html', {
        'active_menu': 'home',
        'friends': friends,
        'pending_received': pending_received,
        'pending_sent': pending_sent,
    })


@login_required(login_url='login')
def search_users(request):
    """AJAX 搜索用户"""
    q = request.GET.get('q', '').strip()
    if len(q) < 2:
        return JsonResponse({'users': []})
    users = User.objects.filter(
        username__icontains=q
    ).exclude(id=request.user.id)[:10]
    return JsonResponse({
        'users': [{'id': u.id, 'username': u.username, 'avatar': u.avatar.url if u.avatar else ''} for u in users]
    })


@login_required(login_url='login')
def send_friend_request(request):
    """发送好友申请"""
    if request.method == 'POST':
        user_id = request.POST.get('user_id', '').strip()
        if not user_id:
            return JsonResponse({'status': 'error', 'msg': '用户ID为空'})
        try:
            to_user = User.objects.get(id=int(user_id))
        except (User.DoesNotExist, ValueError):
            return JsonResponse({'status': 'error', 'msg': '用户不存在'})

        if to_user == request.user:
            return JsonResponse({'status': 'error', 'msg': '不能添加自己为好友'})

        # 检查是否已存在
        existing = Friendship.objects.filter(
            Q(from_user=request.user, to_user=to_user) |
            Q(from_user=to_user, to_user=request.user)
        ).first()
        if existing:
            return JsonResponse({'status': 'error', 'msg': '已存在好友关系或申请'})

        Friendship.objects.create(from_user=request.user, to_user=to_user)
        Notification.objects.create(
            user=to_user, sender=request.user,
            ntype='friend_request',
            content=f'{request.user.username} 想添加你为好友',
            related_url='/accountApp/friends/'
        )
        return JsonResponse({'status': 'ok', 'msg': '好友申请已发送'})
    return JsonResponse({'status': 'error', 'msg': '无效请求'})


@login_required(login_url='login')
def accept_friend_request(request):
    """接受好友申请"""
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        friendship = get_object_or_404(Friendship, from_user_id=user_id, to_user=request.user, status='pending')
        friendship.status = 'accepted'
        friendship.save()
        Notification.objects.create(
            user=friendship.from_user, sender=request.user,
            ntype='friend_accepted',
            content=f'{request.user.username} 通过了你的好友申请',
            related_url='/accountApp/friends/'
        )
        return JsonResponse({'status': 'ok'})


@login_required(login_url='login')
def reject_friend_request(request):
    """拒绝好友申请"""
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        friendship = get_object_or_404(Friendship, from_user_id=user_id, to_user=request.user, status='pending')
        friendship.status = 'rejected'
        friendship.save()
        return JsonResponse({'status': 'ok'})


# ==================== 私聊系统（AJAX 轮询） ====================

@login_required(login_url='login')
def chat_room(request, friend_id):
    """与好友的聊天页面"""
    friend = get_object_or_404(User, id=friend_id)
    # 验证是好友
    Friendship.objects.filter(
        Q(from_user=request.user, to_user=friend) |
        Q(from_user=friend, to_user=request.user),
        status='accepted'
    ).first()  # 仅用于展示，不强制拦截
    messages = PrivateMessage.objects.filter(
        Q(sender=request.user, receiver=friend) |
        Q(sender=friend, receiver=request.user)
    ).order_by('created_at')
    last_id = messages.last().id if messages.exists() else 0
    messages = list(messages[:50])

    # 标记对方发来的消息为已读
    PrivateMessage.objects.filter(sender=friend, receiver=request.user, is_read=False).update(is_read=True)

    return render(request, 'chat_room.html', {
        'active_menu': 'home',
        'friend': friend,
        'messages': messages,
        'last_id': last_id,
    })


@login_required(login_url='login')
def chat_history(request, friend_id):
    """AJAX 加载历史消息"""
    friend = get_object_or_404(User, id=friend_id)
    before_id = request.GET.get('before', 0)
    msgs = PrivateMessage.objects.filter(
        Q(sender=request.user, receiver=friend) |
        Q(sender=friend, receiver=request.user)
    )
    if before_id:
        msgs = msgs.filter(id__lt=before_id)
    msgs = msgs.order_by('-created_at')[:30]
    data = [{
        'id': m.id, 'content': m.content,
        'is_mine': m.sender_id == request.user.id,
        'sender_name': m.sender.username,
        'time': timezone.localtime(m.created_at).strftime('%m-%d %H:%M')
    } for m in reversed(msgs)]
    return JsonResponse({'messages': data})


@login_required(login_url='login')
def send_message(request):
    """AJAX 发送消息"""
    if request.method == 'POST':
        friend_id = request.POST.get('friend_id')
        content = request.POST.get('content', '').strip()
        if not content:
            return JsonResponse({'status': 'error'})
        friend = get_object_or_404(User, id=friend_id)
        msg = PrivateMessage.objects.create(
            sender=request.user, receiver=friend, content=content
        )
        return JsonResponse({
            'status': 'ok',
            'msg': {
                'id': msg.id, 'content': msg.content,
                'is_mine': True,
                'time': timezone.localtime(msg.created_at).strftime('%m-%d %H:%M')
            }
        })


@login_required(login_url='login')
def poll_messages(request):
    """轮询新消息（每 3 秒）"""
    friend_id = request.GET.get('friend_id')
    since_id = request.GET.get('since', 0)
    if not friend_id:
        # 返回所有未读消息数
        count = PrivateMessage.objects.filter(receiver=request.user, is_read=False).count()
        return JsonResponse({'unread_total': count})

    msgs = PrivateMessage.objects.filter(
        receiver=request.user,
        sender_id=friend_id,
        id__gt=since_id
    ).order_by('created_at')
    data = [{
        'id': m.id, 'content': m.content,
        'is_mine': False,
        'sender_name': m.sender.username,
        'time': timezone.localtime(m.created_at).strftime('%m-%d %H:%M')
    } for m in msgs]
    # 标记已读
    msgs.update(is_read=True)
    return JsonResponse({'messages': data})


# ==================== 通知系统 ====================

@login_required(login_url='login')
def notification_list(request):
    """通知列表"""
    notifications = request.user.notifications.all()[:50]
    return render(request, 'notifications.html', {
        'active_menu': 'home',
        'notifications': notifications,
    })


@login_required(login_url='login')
def unread_count(request):
    """AJAX 未读通知数"""
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    msg_count = PrivateMessage.objects.filter(receiver=request.user, is_read=False).count()
    return JsonResponse({'notifications': count, 'messages': msg_count})


@login_required(login_url='login')
def mark_read(request):
    """标记已读 — 通知 + 私信"""
    if request.method == 'POST':
        nid = request.POST.get('id')
        if nid:
            Notification.objects.filter(id=nid, user=request.user).update(is_read=True)
        else:
            # 全部已读：通知 + 私信
            Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
            PrivateMessage.objects.filter(receiver=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'ok'})