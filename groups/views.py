# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from groups.models import groups

@login_required(login_url='/account/login')
def groupsList(request):
    '''
    lista los grupos del usuario registrado
    '''
    if request.user.is_authenticated():
        mygroups = groups.objects.order_by("id")
        ctx = {'TITLE':"Actarium",
               "groups":mygroups
               }
    else:
        ctx = {'TITLE':"Actarium"}
    return render_to_response('groups/list.html',ctx, context_instance = RequestContext(request))

@login_required(login_url='/account/login')
def newGroup(request):
    '''
    crea una nueva organizacion 
    '''
    return render_to_response('groups/new.html',{}, context_instance = RequestContext(request))

@login_required(login_url='/account/login')
def showGroup(request, slug):
    '''
    crea una nueva organizacion 
    '''
    
    q = groups.objects.get(slug=slug)
    #
    ctx = {"group": q}
    return render_to_response('groups/listAct.html', ctx, context_instance = RequestContext(request))
