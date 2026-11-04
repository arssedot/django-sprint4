"""Информационные страницы."""
from django.shortcuts import render


def about(request):
    """Информация о проекте."""
    return render(request, 'pages/about.html')


def rules(request):
    """Правила сайта."""
    return render(request, 'pages/rules.html')
