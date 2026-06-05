from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .models import Note, NoteComment, NoteLike, NoteCollection

# 辅助函数：定义分类映射，确保前端点击能正确显示对应分类
# 假设你的 NOTE_CATEGORIES 是 (1, '旅行踩点指南'), (2, '出行干粮补给'), (3, '躲雨小窝推荐')
def guide(request):
    notes = Note.objects.filter(category=1).order_by('-created_at')
    return render(request, 'guide.html', {
        'notes': notes,
        'active_menu': 'notes',
        'sub_menu': 'guide'
    })

def food(request):
    notes = Note.objects.filter(category=2).order_by('-created_at')
    return render(request, 'food.html', {
        'notes': notes,
        'active_menu': 'notes',
        'sub_menu': 'food'
    })

def stay(request):
    notes = Note.objects.filter(category=3).order_by('-created_at')
    return render(request, 'stay.html', {
        'notes': notes,
        'active_menu': 'notes',
        'sub_menu': 'stay'
    })


@login_required(login_url='login')
def create_note(request):
    """普通用户发布全新游记"""
    if request.method == "POST":
        title = request.POST.get('title')
        summary = request.POST.get('summary')
        content = request.POST.get('content')
        category = request.POST.get('category')
        cover_image = request.FILES.get('cover_image')

        if title and summary and content and category:
            note = Note.objects.create(
                author=request.user,
                title=title,
                summary=summary,
                content=content,
                category=int(category),
                cover_image=cover_image if cover_image else None
            )
            return redirect('noteApp:detail', note_id=note.id)
        else:
            return render(request, 'create_note.html', {
                'error': '喵呜，标题、摘要、正文和分类都是必填项哦！🐾',
                'active_menu': 'notes',
                'sub_menu': 'guide'
            })

    return render(request, 'create_note.html', {
        'active_menu': 'notes',
        'sub_menu': 'guide'
    })


# 下面这些保持不变
def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    # 原子自增阅读量，避免并发覆盖
    Note.objects.filter(id=note_id).update(view_count=F('view_count') + 1)
    note.refresh_from_db()
    comments = note.comments.filter(parent__isnull=True)
    return render(request, 'note_detail.html', {
        'note': note,
        'comments': comments,
        'active_menu': 'notes'
    })

@login_required
def like_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    like, created = NoteLike.objects.get_or_create(note=note, user=request.user)
    if created:
        note.like_count += 1
        note.save()
        status = 'liked'
    else:
        like.delete()
        note.like_count -= 1
        note.save()
        status = 'unliked'
    return JsonResponse({'status': status, 'count': note.like_count})


@login_required
def collect_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    collection, created = NoteCollection.objects.get_or_create(note=note, user=request.user)
    if created:
        note.collect_count += 1
        note.save()
        status = 'collected'
    else:
        collection.delete()
        note.collect_count -= 1
        note.save()
        status = 'uncollected'
    return JsonResponse({'status': status, 'count': note.collect_count})


@login_required
def add_comment(request, note_id):
    if request.method == 'POST':
        note = get_object_or_404(Note, id=note_id)
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        parent_comment = None
        if parent_id:
            parent_comment = get_object_or_404(NoteComment, id=parent_id)
        NoteComment.objects.create(
            note=note, user=request.user, content=content, parent=parent_comment
        )
    return redirect('noteApp:detail', note_id=note_id)