"""Информационные страницы и обработчики ошибок."""
from django.shortcuts import render
from django.views.generic import TemplateView


class AboutView(TemplateView):
    """Информация о проекте."""

    template_name = 'pages/about.html'


class RulesView(TemplateView):
    """Правила сайта."""

    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    """Страница отсутствует."""
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    """Внутренняя ошибка сервера."""
    return render(request, 'pages/500.html', status=500)


def csrf_failure(request, reason=''):
    """Ошибка проверки CSRF-токена."""
    return render(request, 'pages/403csrf.html', status=403)
