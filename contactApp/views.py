from django.shortcuts import render
# 从当前的 models.py 中引入刚刚建好的 Feedback 模型
from .models import Feedback 

def cooperate(request):
    # 商务合作页面依然保持原样
    return render(request, 'cooperate.html', {
        'active_menu': 'contact', 
        'sub_menu': 'cooperate'
    })


def feedback(request):
    # 初始化上下文环境，把原本的高亮参数带上
    context = {
        'active_menu': 'contact',
        'sub_menu': 'feedback'
    }
    
    # 判断用户是否点击了“投递信件”按钮发送了 POST 请求
    if request.method == 'POST':
        # 1. 抓取前端表单数据
        f_type = request.POST.get('feedback_type')
        name = request.POST.get('nickname')
        email = request.POST.get('email')
        msg = request.POST.get('content')
        
        # 2. 保存到我们完美的 contactapp_feedback 表中
        fb = Feedback(feedback_type=f_type, nickname=name, email=email, content=msg)
        fb.save()
        
        # 3. 把治愈系的投递成功提示塞入上下文中
        context['success_msg'] = '📬 喵！信件已安全投入信箱，小猫正在火速送往后台！'
        
    return render(request, 'feedback.html', context)