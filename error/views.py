from django.shortcuts import render, render_to_response
from django.template import RequestContext


def page_not_found(request, exception=None):
    return render(request, 'error/404page.html', status=404)


def server_error(request, exception=None):
    return render(request, 'error/500page.html', status=500)
