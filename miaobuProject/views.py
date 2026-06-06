import os
import requests
import dashscope
from django.http import JsonResponse
from dotenv import load_dotenv

# 加载 .env 文件中的配置
load_dotenv()
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

# 绕过系统代理（解决 Windows 代理配置导致的 dashscope 连接失败）
_original_session_init = requests.Session.__init__


def _patched_init(self, *args, **kwargs):
    _original_session_init(self, *args, **kwargs)
    self.trust_env = False


requests.Session.__init__ = _patched_init


def chat_ai(request):
    user_input = request.GET.get('message', '')
    if not user_input:
        return JsonResponse({'reply': '喵~ 你还没输入内容呢！'})

    try:
        response = dashscope.Generation.call(
            model='qwen-turbo',
            messages=[{'role': 'user', 'content': user_input}]
        )
        if response.status_code == 200:
            return JsonResponse({'reply': response.output.text})
        else:
            return JsonResponse({'reply': f'哎呀，出错了: {response.message}'})
    except Exception as e:
        return JsonResponse({'reply': '喵呜…连接AI失败了，可能是网络问题，稍后再试吧~ 🐾'})
