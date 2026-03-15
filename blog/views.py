from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q

from .models import Post, Category, Comment, Like
from .forms import PostForm, CommentForm


def home(request):
    posts = Post.objects.filter(status=Post.STATUS_PUBLISHED).select_related('author', 'category')
    categories = Category.objects.all()

    # Search
    query = request.GET.get('q')
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(body__icontains=query))

    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'blog/home.html', {
        'posts': posts,
        'categories': categories,
        'query': query,
    })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.STATUS_PUBLISHED)
    comments = post.comments.filter(is_approved=True)
    comment_form = CommentForm()
    liked = False

    if request.user.is_authenticated:
        liked = Like.objects.filter(post=post, user=request.user).exists()

    related_posts = Post.objects.filter(
        status=Post.STATUS_PUBLISHED,
        category=post.category
    ).exclude(id=post.id)[:3]

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'liked': liked,
        'related_posts': related_posts,
    })


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if post.status == Post.STATUS_PUBLISHED:
                post.published_at = timezone.now()
            post.save()
            form.save_m2m()
            messages.success(request, 'Post created successfully!')
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Create'})


@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if post.status == Post.STATUS_PUBLISHED and not post.published_at:
                post.published_at = timezone.now()
            post.save()
            form.save_m2m()
            messages.success(request, 'Post updated successfully!')
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Edit', 'post': post})


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
        return redirect('blog:home')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.STATUS_PUBLISHED)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added!')
    return redirect(post.get_absolute_url())


@login_required
def toggle_like(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.STATUS_PUBLISHED)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'count': post.likes.count()})


@login_required
def dashboard(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/dashboard.html', {'posts': posts})
