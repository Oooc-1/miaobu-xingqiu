from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Album, Photo
from noteApp.models import NoteLike, NoteCollection


# 通用登录与身份自动分流
def login_view(request):
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)

        if user is not None:
            login(request, user)
            # 自动识别：如果是管理员，直接重定向到薄荷绿的"核心中控台"
            if user.is_superuser or user.is_staff:
                return redirect('admin:index')
            else:
                # 如果是普通用户，重定向回前台首页
                return redirect('home')
        else:
            # 扁平路径，并加上基础模板所需的高亮菜单暗号
            return render(request, 'login.html', {
                'error': '喵呜，暗号或密码错啦！🐾',
                'active_menu': 'home'
            })

    return render(request, 'login.html', {'active_menu': 'home'})


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

    return render(request, 'my_nest.html', {
        'user': request.user,
        'active_menu': 'home',
        'liked_notes': liked_notes,
        'collected_notes': collected_notes,
    })


@login_required(login_url='login')
def change_avatar(request):
    if request.method == "POST":
        new_avatar = request.FILES.get('avatar_file')
        if new_avatar:
            # 直接把图片赋给当前登录的用户对象
            request.user.avatar = new_avatar
            request.user.save()  # 保存更改
            return render(request, 'change_avatar.html', {
                'success': '喵呜！新头像保存成功啦！✨',
                'active_menu': 'home'
            })
        else:
            return render(request, 'change_avatar.html', {
                'error': '你好像还没有选择任何猫片哦？🐾',
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