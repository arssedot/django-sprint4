"""Публичные страницы блога."""
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post

POSTS_ON_MAIN = 5


def published_posts():
    """Вернуть опубликованные посты с доступной категорией."""
    return Post.objects.select_related(
        'author', 'category', 'location',
    ).filter(
        is_published=True, category__is_published=True,
        pub_date__lte=timezone.now(),
    )


def index(request):
    """Показать пять последних публикаций."""
    return render(request, 'blog/index.html', {
        'post_list': published_posts()[:POSTS_ON_MAIN],
    })


def category_posts(request, category_slug):
    """Показать публикации доступной категории."""
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True,
    )
    return render(request, 'blog/category.html', {
        'category': category,
        'post_list': published_posts().filter(category=category),
    })


def post_detail(request, post_id):
    """Показать доступную публикацию или ответить 404."""
    return render(request, 'blog/detail.html', {
        'post': get_object_or_404(published_posts(), pk=post_id),
    })
