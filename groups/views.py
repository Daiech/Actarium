# Create your views here.
#encoding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from groups.models import groups, group_type, rel_user_group, minutes, invitations
from groups.forms import newGroupForm
#from django.core.mail import EmailMessage
import re


@login_required(login_url='/account/login')
def groupsList(request):
    '''
    lista los grupos del usuario registrado
    '''
    try:
        mygroups = groups.objects.filter(rel_user_group__id_user=request.user, rel_user_group__is_active=True)
    except ObjectDoesNotExist:
        mygroups = "Either the entry or blog doesn't exist."

    ctx = {'TITLE': "Actarium", "groups": mygroups}
    return render_to_response('groups/list.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def newGroup(request):
    '''
        crea una nuevo grupo
    '''

    if request.method == "POST":
        form = newGroupForm(request.POST)
        if form.is_valid():
            df = {
                'name': form.cleaned_data['name'],
                'description': form.cleaned_data['description'],
                'id_creator': request.user
            }
            myNewGroup = groups(name=df['name'],
                           description=df['description'],
                           id_creator=df['id_creator'],
                           id_group_type=group_type.objects.get(pk=1),
                         )
            myNewGroup.save()
            rel_user_group(id_user=request.user, id_group=myNewGroup).save()
            return HttpResponseRedirect("/groups/" + str(myNewGroup.slug))
    else:
        form = newGroupForm()

    ctx = {'TITLE': "Actarium",
           "newGroupForm": form,
           }
    return render_to_response('groups/newGroup.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def showGroup(request, slug):
    '''
        Muestra la informacion de un grupo
    '''
    q = groups.objects.get(slug=slug)
    is_member = rel_user_group.objects.filter(id_group=q.id, id_user=request.user)
    if is_member:
        mem = rel_user_group.objects.filter(id_group=q.id, is_active=True)
        minutes_group = minutes.objects.filter(id_group=q.id)
        #inv = newInvitationUser("maizaga@daiech.com", request.user, q)
        ctx = {'TITLE': q.name, "group": q, "members": mem, "minutes": minutes_group}
        return render_to_response('groups/showGroup.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/#error-view-group')


def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email):
            return True
        else:
            return False
    else:
        return False


def sendInvitationUser(email, user, group):
    '''
        Enviar una invitacion a un usuario via email
    '''
    if validateEmail(email):
        invitation = invitations(email_invited=email, id_user_from=user, id_group=group)
        invitation.save()
        return True
    else:
        return False


#@requires_csrf_token #pilas con esto, es para poder enviar los datos via POST 
def newInvitation(request):
    if request.is_ajax():
        if request.method == 'GET':
            q = groups.objects.get(pk=request.GET['pk'])
            mail = str(request.GET['search'])
            if sendInvitationUser(mail, request.user, q):
                message = "Se ha enviado la invitación a " + str(mail)
            else:
                message = "Error en el correo"
    else:
        message = "Error"
    return HttpResponse(message)
