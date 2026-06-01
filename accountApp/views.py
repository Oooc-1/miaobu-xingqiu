from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# 通用登录与身份自动分流
def login_view(request):
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            login(request, user)
            # 自动识别：如果是管理员，直接重定向到薄荷绿的“核心中控台”
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
    # 扁平路径，直来直去
    return render(request, 'my_nest.html', {
        'user': request.user,
        'active_menu': 'home' # 也可以改成你需要的其它高亮ID
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