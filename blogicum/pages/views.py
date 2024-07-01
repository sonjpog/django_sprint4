from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView


class AboutView(TemplateView):
    template_name = 'pages/about.html'


class RulesView(TemplateView):
    template_name = 'pages/rules.html'


def csrf_failure(request, reason='') -> HttpResponse:
    template = 'pages/403csrf.html'
    return render(request, template, status=403)


def page_not_found(request, exception) -> HttpResponse:
    template = 'pages/404.html'
    return render(request, template, status=404)


def server_error(request, reason='') -> HttpResponse:
    template = 'pages/500.html'
    return render(request, template, status=500)
