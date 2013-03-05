from django.shortcuts import render_to_response
from django.template import RequestContext


def explode(request):
    raise Exception('boom!')


def home(request):
    context = {}
    return render_to_response(
        'baseline/home.html', context, context_instance=RequestContext(request))


def notfound(request):
    from django.http import Http404
    raise Http404


def preview(request, template):
    context = {}
    return render_to_response(
        template, context, context_instance=RequestContext(request))


def static_page(request):
    # strip off leading slash
    template = request.path[1:]

    # strip off trailing slash if it's there
    if template[-1] == '/':
        template = template[:-1]

    # if there is no extension, append .html
    if '.' not in template:
        template += '.html'

    return render_to_response(template)
