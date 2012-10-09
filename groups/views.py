# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

#from groups.models import groups

@login_required(login_url='/account/login')
def list(request):
    '''
    lista las organizaciones del usuario registrado
    '''
    if request.user.is_authenticated():
        #org = groups.objects.order_by("id")
        ctx = {'TITLE':"Actarium",
               #"org":org
               }
    else:
        ctx = {'TITLE':"Actarium"}
    return render_to_response('groups/list.html',{}, context_instance = RequestContext(request))

@login_required(login_url='/account/login')
def new(request):
    '''
    crea una nueva organizacion 
    '''
    return render_to_response('groups/new.html',{}, context_instance = RequestContext(request))

@login_required(login_url='/account/login')
def listMinutes(request):
    '''
    crea una nueva organizacion 
    '''
    return render_to_response('groups/listAct.html',{}, context_instance = RequestContext(request))
