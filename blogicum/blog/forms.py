"""Формы публикаций, комментариев и профиля."""
from django import forms

from .models import Comment, Post, User


class PostForm(forms.ModelForm):
    """Создание и редактирование публикации."""

    class Meta:
        model = Post
        fields = ('title', 'text', 'pub_date', 'category', 'location', 'image')
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'},
            ),
        }


class CommentForm(forms.ModelForm):
    """Текст комментария."""

    class Meta:
        model = Comment
        fields = ('text',)


class ProfileForm(forms.ModelForm):
    """Изменение только собственных данных пользователя."""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
