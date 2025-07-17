from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Thread, Post
from .forms import ThreadForm, PostForm

@login_required
def index(request):
    categories = Category.objects.all()
    return render(request, 'forum/index.html', {'categories': categories})

@login_required
def thread_list(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    threads = Thread.objects.filter(category=category).order_by('-created_at')
    return render(request, 'forum/thread_list.html', {'category': category, 'threads': threads})

@login_required
def post_list(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    posts = Post.objects.filter(thread=thread).order_by('created_at')
    form = PostForm()
    return render(request, 'forum/post_list.html', {'thread': thread, 'posts': posts, 'form': form})

@login_required
def create_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return redirect('forum:thread_list', category_id=thread.category.id)
    else:
        form = ThreadForm()
    return render(request, 'forum/create_thread.html', {'form': form})

@login_required
def create_post(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.author = request.user
            post.save()
            return redirect('forum:post_list', thread_id=thread.id)
    return redirect('forum:post_list', thread_id=thread.id)

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        messages.error(request, "You are not authorized to edit this post.")
        return redirect('forum:post_list', thread_id=post.thread.id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully.")
            return redirect('forum:post_list', thread_id=post.thread.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'forum/post_edit.html', {'form': form, 'post': post})

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        messages.error(request, "You are not authorized to delete this post.")
        return redirect('forum:post_list', thread_id=post.thread.id)

    if request.method == 'POST':
        thread_id = post.thread.id
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect('forum:post_list', thread_id=thread_id)
    return redirect('forum:post_list', thread_id=post.thread.id)