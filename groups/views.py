# Create your views here.
#encoding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from groups.models import groups, group_type, rel_user_group, minutes, invitations, minutes_type_1, minutes_type, reunions
from groups.forms import newGroupForm, newMinutesForm, newReunionForm
#from django.core.mail import EmailMessage
import re
import datetime
from django.utils.timezone import make_aware, get_default_timezone

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
    q = groups.objects.get(slug=slug, is_active=True)
    is_member = rel_user_group.objects.filter(id_group=q.id, id_user=request.user)
    if is_member:
        members = rel_user_group.objects.filter(id_group=q.id, is_active=True)
        minutes_group = minutes.objects.filter(id_group=q.id)
        ctx = {'TITLE': q.name, "group": q, "members": members, "minutes": minutes_group}
        return render_to_response('groups/showGroup.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/groups/#error-view-group')


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


#@requires_csrf_token  # pilas con esto, es para poder enviar los datos via POST
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


def newMinutes(request,slug):
    q = groups.objects.get(slug=slug, is_active=True)
    is_member = rel_user_group.objects.filter(id_group=q.id, id_user=request.user)
    if is_member:
        if request.method == "POST":
            form = newMinutesForm(request.POST)
            if form.is_valid():
                df = {
                'code': form.cleaned_data['code'],
                'date_start': form.cleaned_data['date_start'],
                'date_end': form.cleaned_data['date_end'],
                'location': form.cleaned_data['location'],
                'agenda': form.cleaned_data['agenda'],
                'agreement': form.cleaned_data['agreement'],
                }
                myNewMinutes_type_1 = minutes_type_1(
                               date_start=datetime.datetime.strptime(str(datetime.date.today()) + " "+str(df['date_start']),'%Y-%m-%d %H:%M:%S'),
                               date_end=datetime.datetime.strptime(str(datetime.date.today()) + " "+str(df['date_end']),'%Y-%m-%d %H:%M:%S'),
                               location=df['location'],
                               agenda=df['agenda'],
                               agreement = df['agreement'],
                             )
                myNewMinutes_type_1.save()
                myNewMinutes = minutes(
                                code = df['code'],
                                id_extra_minutes = myNewMinutes_type_1,
                                id_group = q,
                                id_type = minutes_type.objects.get(pk=1),
                            )
                myNewMinutes.save()
                return HttpResponseRedirect("/groups/" + str(q.slug))
        else:
            form = newMinutesForm()
        ctx = {'TITLE': "Actarium",
               "newMinutesForm": form,
               }
        return render_to_response('groups/newMinutes.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/groups/#error-view-group')

def newReunion(request,slug):
    q = groups.objects.get(slug=slug, is_active=True)
    is_member = rel_user_group.objects.filter(id_group=q.id, id_user=request.user)
    if is_member:
        if request.method == "POST":
            form = newReunionForm(request.POST)
            if form.is_valid():
                df = {
                    'date_reunion': form.cleaned_data['date_reunion'],
                    'agenda': form.cleaned_data['agenda'],
                }
                myNewReunion = reunions(
                               id_convener = request.user,
                               date_reunion=df['date_reunion'],
                               id_group = q,
                               agenda=df['agenda'],
                             )
                myNewReunion.save()
                return HttpResponseRedirect("/groups/" + str(q.slug))
#                ctx = {'TITLE': "Actarium",
#                       "newReunionForm": form,
#                       "date_reunion":df['date_reunion'],
#                       "agenda":df['agenda'],
#                }
#                return render_to_response('groups/newReunion.html', ctx, context_instance=RequestContext(request))
        else:
            form = newReunionForm()
        ctx = {'TITLE': "Actarium",
               "newReunionForm": form,
               }
        return render_to_response('groups/newReunion.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/groups/#error-view-group')

def calendar(request):
    gr = groups.objects.filter(rel_user_group__id_user=request.user) #grupos
    my_reu = reunions.objects.filter(id_group__in=gr, is_done=False) #reuniones
    ctx = {'TITLE': "Actarium",
       "reunions_day": my_reu,
       "reunions": my_reu,
           }
    return render_to_response('groups/calendar.html', ctx, context_instance=RequestContext(request))

def calendarDate(request, slug=None):
    gr = groups.objects.filter(rel_user_group__id_user=request.user) #grupos
    my_reu = reunions.objects.filter(id_group__in=gr, is_done=False) #reuniones

    dateslug_min = str(make_aware(datetime.datetime.strptime(slug+" 00:00:00",'%Y-%m-%d %H:%M:%S'),get_default_timezone()))
    dateslug_max = str(make_aware(datetime.datetime.strptime(slug+" 23:59:59",'%Y-%m-%d %H:%M:%S'),get_default_timezone()))
    my_reu_day = reunions.objects.filter(id_group__in=gr,date_reunion__range = [dateslug_min,dateslug_max]) #reuniones para un dia
    ctx = {'TITLE': "Actarium",
       "reunions_day": my_reu_day,
       "reunions": my_reu,}

    
    return render_to_response('groups/calendar.html', ctx, context_instance=RequestContext(request))