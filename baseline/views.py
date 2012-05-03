from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

def explode(request):
    raise Exception('boom!')

def home(request):
    context = {}
    return render_to_response('baseline/home.html', context,
                       context_instance=RequestContext(request))

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

def notfound(request):
    from django.http import Http404
    raise Http404

def preview(request, template):
    context = {}
    return render_to_response(template, context,
                       context_instance=RequestContext(request))
