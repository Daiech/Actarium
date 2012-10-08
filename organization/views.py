# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from organization.models import organizations

@login_required(login_url='/account/login')
def list(request):
    '''
    lista las organizaciones del usuario registrado
    '''
    if request.user.is_authenticated():
        org = organizations.objects()
        ctx = {'TITLE':"Actarium","org":org}
    else:
        ctx = {'TITLE':"Actarium"}
    return render_to_response('organization/list.html',{}, context_instance = RequestContext(request))

@login_required(login_url='/account/login')
def new(request):
    '''
    crea una nueva organizacion 
    '''
    return render_to_response('organization/new.html',{}, context_instance = RequestContext(request))

