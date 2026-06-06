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

# 系统提示词：喵喵人设
SYSTEM_PROMPT = {
    'role': 'system',
    'content': (
        '你是一只名叫"喵喵"的旅游小助手，住在喵步星球上。'
        '回答问题时要用猫咪的语气，多用"喵"字，可爱亲切一点。'
        '你熟悉喵步星球的各个板块：漫步地图（城市探险、森林探险、巷弄巡逻）、'
        '铲屎官笔记（踩点指南、干粮补给、躲雨小窝）、'
        '肉垫体验（逗猫棒活动、藏宝阁周边）、喵眼世界（今日鱼干、追光日记）。'
        '回答要简短有条理，适当使用 Markdown 格式（标题、列表）让排版更清晰。'
    )
}

MAX_HISTORY = 10  # 保留最近 10 轮对话


def chat_ai(request):
    user_input = request.GET.get('message', '')
    if not user_input:
        return JsonResponse({'reply': '喵~ 你还没说话呢！🐾'})

    # 1. 获取或初始化会话历史
    if 'chat_history' not in request.session:
        request.session['chat_history'] = [SYSTEM_PROMPT]

    # 2. 将当前用户输入加入历史
    request.session['chat_history'].append({'role': 'user', 'content': user_input})

    # 限制历史记录条数（保留 system 提示词 + 最近 N 轮）
    history = request.session['chat_history']
    if len(history) > MAX_HISTORY * 2 + 1:
        request.session['chat_history'] = [history[0]] + history[-(MAX_HISTORY * 2):]

    try:
        # 3. 将完整历史发送给 AI
        response = dashscope.Generation.call(
            model='qwen-turbo',
            messages=request.session['chat_history']
        )

        if response.status_code == 200:
            ai_reply = response.output.text
            # 4. 将 AI 回复也存入历史
            request.session['chat_history'].append(
                {'role': 'assistant', 'content': ai_reply}
            )
            request.session.modified = True
            return JsonResponse({'reply': ai_reply})
        else:
            return JsonResponse({'reply': f'喵呜…出错了: {response.message}'})

    except Exception as e:
        return JsonResponse({'reply': '喵呜…网络好像开小差了！稍后再试试吧~ 🐾'})
