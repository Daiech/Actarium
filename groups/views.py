# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from groups.models import groups,group_type
from groups.forms import newGroupForm
import datetime

@login_required(login_url='/account/login')
def groupsList(request):
    '''
    lista los grupos del usuario registrado
    '''
    if request.user.is_authenticated():
        mygroups = groups.objects.all()
        try:
            mygroups = groups.objects.filter(id_creator=request.user.id)
        except ObjectDoesNotExist:
            print("Either the entry or blog doesn't exist.")
            mygroups = "Either the entry or blog doesn't exist."
        
        ctx = {'TITLE':"Actarium",
               "groups":mygroups,
               }
    else:
        ctx = {'TITLE':"Actarium"}
    return render_to_response('groups/list.html',ctx, context_instance = RequestContext(request))

@login_required(login_url='/account/login')
def newGroup(request):
    '''
    crea una nueva organizacion 
    '''
    if request.method == "POST":
        form = newGroupForm(request.POST)
        if form.is_valid():
            df = {
                'name': form.cleaned_data['name'],
                'description': form.cleaned_data['description'],
                'id_creator' : request.user
            }
            query = groups(name= df['name'],
                           description= df['description'],
                           id_creator = df['id_creator'],
                           id_group_type = group_type.objects.get(pk=1),
                         )
            query.save()
            return HttpResponseRedirect("/groups/"+str(query.slug))
    else:
        form = newGroupForm()
        
    ctx = {'TITLE':"Actarium",
           "newGroupForm":form,
           }
    return render_to_response('groups/new.html',ctx, context_instance = RequestContext(request))

@login_required(login_url='/account/login')
def showGroup(request, slug):
    '''
    crea una nueva organizacion 
    '''
    
    q = groups.objects.get(slug=slug)
    #
    ctx = {"group": q}
    return render_to_response('groups/listAct.html', ctx, context_instance = RequestContext(request))
