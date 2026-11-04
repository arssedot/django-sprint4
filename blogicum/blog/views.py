"""Публичные страницы и формы блога."""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView

from .forms import CommentForm, PostForm, ProfileForm
from .models import Category, Comment, Post, User

POSTS_PER_PAGE = 10


def post_queryset():
    """Получить посты с авторами, категориями и числом комментариев."""
    return Post.objects.select_related(
        'author', 'category', 'location',
    ).annotate(comment_count=Count('comments')).order_by('-pub_date', '-pk')


def published_posts():
    """Отфильтровать доступные всем публикации."""
    return post_queryset().filter(
        is_published=True, category__is_published=True,
        pub_date__lte=timezone.now(),
    )


def page_for(request, posts):
    """Сформировать страницу пагинации."""
    return Paginator(posts, POSTS_PER_PAGE).get_page(request.GET.get('page'))


def index(request):
    """Показать последние опубликованные записи."""
    return render(request, 'blog/index.html', {
        'page_obj': page_for(request, published_posts()),
    })


def category_posts(request, category_slug):
    """Показать записи доступной категории."""
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True,
    )
    return render(request, 'blog/category.html', {
        'category': category,
        'page_obj': page_for(
            request, published_posts().filter(category=category),
        ),
    })


def profile(request, username):
    """Показать профиль и доступные посетителю посты автора."""
    author = get_object_or_404(User, username=username)
    posts = post_queryset() if request.user == author else published_posts()
    return render(request, 'blog/profile.html', {
        'profile': author,
        'page_obj': page_for(request, posts.filter(author=author)),
    })


def visible_post(request, post_id):
    """Автор видит свой черновик; остальные — опубликованный пост."""
    post = get_object_or_404(post_queryset(), pk=post_id)
    if request.user != post.author:
        post = get_object_or_404(published_posts(), pk=post_id)
    return post


def post_detail(request, post_id):
    """Показать пост, форму и список комментариев."""
    post = visible_post(request, post_id)
    return render(request, 'blog/detail.html', {
        'post': post, 'form': CommentForm(),
        'comments': post.comments.select_related('author'),
    })


@login_required
def create_post(request):
    """Создать публикацию от имени текущего пользователя."""
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_post(request, post_id):
    """Редактировать пост может только его автор."""
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id=post_id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def delete_post(request, post_id):
    """Подтвердить и удалить собственный пост."""
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', {
        'form': PostForm(instance=post),
    })


@login_required
def add_comment(request, post_id):
    """Добавить комментарий к доступной публикации."""
    post = visible_post(request, post_id)
    form = CommentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    """Редактировать можно только собственный комментарий."""
    comment = get_object_or_404(
        Comment, pk=comment_id, post_id=post_id, author=request.user,
    )
    form = CommentForm(request.POST or None, instance=comment)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', {
        'form': form, 'comment': comment,
    })


@login_required
def delete_comment(request, post_id, comment_id):
    """Подтвердить и удалить собственный комментарий."""
    comment = get_object_or_404(
        Comment, pk=comment_id, post_id=post_id, author=request.user,
    )
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', {'comment': comment})


@login_required
def edit_profile(request):
    """Изменить профиль текущего пользователя."""
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('blog:profile', username=form.instance.username)
    return render(request, 'blog/user.html', {'form': form})


class RegistrationView(CreateView):
    """Регистрация стандартного пользователя Django."""

    form_class = UserCreationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('login')
