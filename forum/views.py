from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import PlaylistPost, Comment
from .forms import PlaylistPostForm, CommentForm

@login_required
def post_list(request):
    """
    플레이리스트 게시물 목록
    """
    posts = PlaylistPost.objects.all().select_related('author', 'playlist')
    return render(request, 'forum/post_list.html', {'posts': posts})

@login_required
def post_detail(request, post_id):
    """
    플레이리스트 게시물 상세 페이지
    """
    post = get_object_or_404(PlaylistPost, pk=post_id)
    comment_form = CommentForm()
    comments = post.comments.all().select_related('author')
    return render(request, 'forum/post_detail.html', {
        'post': post,
        'comment_form': comment_form,
        'comments': comments
    })

@login_required
def post_create(request):
    """
    플레이리스트 게시물 생성
    """
    if request.method == 'POST':
        form = PlaylistPostForm(request.POST, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, '게시물이 성공적으로 등록되었습니다.')
            return redirect('forum:post_detail', post_id=post.id)
    else:
        form = PlaylistPostForm(user=request.user)
    return render(request, 'forum/post_form.html', {'form': form})

@login_required
def post_edit(request, post_id):
    """
    플레이리스트 게시물 수정
    """
    post = get_object_or_404(PlaylistPost, pk=post_id, author=request.user)
    if request.method == 'POST':
        form = PlaylistPostForm(request.POST, instance=post, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '게시물이 성공적으로 수정되었습니다.')
            return redirect('forum:post_detail', post_id=post.id)
    else:
        form = PlaylistPostForm(instance=post, user=request.user)
    return render(request, 'forum/post_form.html', {'form': form, 'post': post})

@login_required
@require_POST
def post_delete(request, post_id):
    """
    플레이리스트 게시물 삭제
    """
    post = get_object_or_404(PlaylistPost, pk=post_id, author=request.user)
    post.delete()
    messages.success(request, '게시물이 삭제되었습니다.')
    return redirect('forum:post_list')

@login_required
@require_POST
def add_comment(request, post_id):
    """
    댓글 추가
    """
    post = get_object_or_404(PlaylistPost, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        messages.success(request, '댓글이 등록되었습니다.')
    else:
        messages.error(request, '댓글 작성에 실패했습니다.')
    return redirect('forum:post_detail', post_id=post.id)

@login_required
@require_POST
def toggle_like(request, post_id):
    """
    게시물 좋아요 토글
    """
    post = get_object_or_404(PlaylistPost, pk=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
    return JsonResponse({'liked': liked, 'total_likes': post.total_likes()})
