# Create your views here.
#encoding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from groups.models import groups, group_type, rel_user_group, minutes, invitations, minutes_type_1, minutes_type, reunions, admin_group, assistance
from groups.forms import newGroupForm, newMinutesForm, newReunionForm
from django.contrib.auth.models import User
#from django.core.mail import EmailMessage
import re
import datetime
from django.utils.timezone import make_aware, get_default_timezone, make_naive
from django.utils import simplejson as json
from account.templatetags.gravatartag import showgravatar
from django.core import serializers


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
                'id_creator': request.user,
                'id_group_type': form.cleaned_data['id_group_type']
            }
            myNewGroup = groups(name=df['name'],
                           description=df['description'],
                           id_creator=df['id_creator'],
                           id_group_type=group_type.objects.get(pk=df['id_group_type']),
                         )
            myNewGroup.save()
            rel_user_group(id_user=request.user, id_group=myNewGroup).save()
            admin_group(id_user=request.user, id_group=myNewGroup).save()
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
        members_pend = invitations.objects.filter(id_group=q.id, is_active=True)
        minutes_group = minutes.objects.filter(id_group=q.id)
        ctx = {'TITLE': q.name, "group": q, "members": members, "minutes": minutes_group, "members_pend": members_pend}
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


@login_required(login_url='/account/login')
def getMembers(request):
    if request.is_ajax():
        if request.method == "GET":
            try:
                search = str(request.GET['search'])
                if validateEmail(search):
                    try:
                        ans = User.objects.get(email=search)
                    except User.DoesNotExist:
                        ans = 1  # email valido, pero no es usuario
                else:
                    try:
                        ans = User.objects.get(username=search)
                    except User.DoesNotExist:
                        ans = 2  # no existe el usuario
                if ans != 1 and ans != 2:
                    message = {
                        "mail_is_valid": True,
                        "username": ans.username,
                        "mail": ans.email,
                        "gravatar": showgravatar(ans.email, 30)}
                else:
                    if ans == 1:
                        message = {"mail_is_valid": True, "mail": search, "username": False}
                    else:
                        if ans == 2:
                            message = {"mail_is_valid": False}
                        else:
                            message = False
            except Exception:
                message = False
            return HttpResponse(json.dumps(message), mimetype="application/json")
        else:
            message = False
        return HttpResponse(message)
    else:
        message = False
        return HttpResponse(message)


def sendInvitationUser(email, user, group):
    '''
        Enviar una invitacion a un usuario via email
    '''
    if validateEmail(email):
        invitation, created = invitations.objects.get_or_create(email_invited=email, id_user_from=user, id_group=group, is_active=True)
        if created:
            #  send email here
            return invitation
        else:
            return False
    else:
        return 0  # Email Failed


def isMemberOfGroup(id_user, id_group):
    try:
        is_member = rel_user_group.objects.filter(id_user=id_user, id_group=id_group)
        if is_member:
            return True
    except User.DoesNotExist, e:
        print e
        return False


def isMemberOfGroupByEmail(email, id_group):
    if validateEmail(email):
        try:
            ans = User.objects.get(email=email)
        except User.DoesNotExist, e:
            print e
            return False
        if ans:
            return isMemberOfGroup(ans, id_group)
    else:
        return False


#@requires_csrf_token  # pilas con esto, es para poder enviar los datos via POST
@login_required(login_url='/account/login')
def newInvitation(request):
    if request.is_ajax():
        if request.method == 'GET':
            try:
                q = groups.objects.get(pk=request.GET['pk'])
                if not isMemberOfGroup(request.user, q):
                    return HttpResponse(q)
            except groups.DoesNotExist:
                q = False
                return HttpResponse(q)
            mail = str(request.GET['search'])
            if isMemberOfGroupByEmail(mail, q):
                invited = False
                message = "El usuario ya es miembro del grupo"
                iid = False
                gravatar = False
            else:
                inv = sendInvitationUser(mail, request.user, q)
                if inv and not inv is 0:
                    invited = True
                    iid = str(inv.id)
                    gravatar = showgravatar(mail, 30)
                    message = "Se ha enviado la invitación a " + str(mail) + " al grupo " + str(q.name)
                else:
                    iid = False
                    invited = False
                    gravatar = False
                    if not inv and not inv is 0:
                        message = "El usuario tiene la invitación pendiente"
                    else:
                        if inv == 0:
                            message = "El correo electronico no es valido"
                        else:
                            message = "Error desconocido. Lo sentimos"
            response = {"invited": invited, "message": message, "email": mail, "iid": iid, "gravatar": gravatar}
    else:
        response = "Error invitacion"
    return HttpResponse(json.dumps(response), mimetype="application/json")


@login_required(login_url='/account/login')
def acceptInvitation(request):
    if request.is_ajax():
        if request.method == 'GET':
            try:
                if request.GET['i_id'][0] == 's':
                    accept = True
                else:
                    if request.GET['i_id'][0] == 'n':
                        accept = False
                    else:
                        return HttpResponse(False)  # error 1, peticion sin controlador s o n
                iid = request.GET['i_id'][1:]
                print "inv id= %s" % (str(iid))
                try:
                    inv = invitations.objects.get(id=iid)
                    is_member = isMemberOfGroup(inv.id_user_from, inv.id_group)
                except invitations.DoesNotExist:
                    inv = False
                    is_member = False
                if accept and is_member and inv:  # aprobar la invitacion
                    rel_user_group(id_user=request.user, id_group=inv.id_group).save()
                    inv.is_active = False
                    inv.save()
                    accepted = True
                    group = {"id": inv.id_group.id, "name": inv.id_group.name, "slug": "/groups/" + inv.id_group.slug, "img_group": inv.id_group.img_group}
                    message = "Aceptar la solicitud"
                else:  # no aprobar la invitacion
                    if inv and not accept:
                        inv.is_active = False
                        inv.save()
                        accepted = False
                        group = {"id": inv.id_group.id, "name": inv.id_group.name, "slug": "/groups/" + inv.id_group.slug, "img_group": inv.id_group.img_group}
                        message = "NO Aceptar la solicitud"
                    else:
                        return HttpResponse(inv)
                response = {"accepted": accepted, "message": message, "group": group}
            except Exception, e:
                print e
                return HttpResponse(False)
    else:
        response = "Error invitacion is not AJAX"
    return HttpResponse(json.dumps(response), mimetype="application/json")


@login_required(login_url='/account/login')
def deleteInvitation(request):
    if request.is_ajax():
        if request.method == 'GET':
            try:
                iid = request.GET['id_inv']
                if iid == "" or iid == None:
                    return HttpResponse(False)
                try:
                    inv = invitations.objects.get(id=iid, is_active=True)
                except invitations.DoesNotExist:
                    inv = False
                if inv:  # si eliminar la invitacion
                    inv.is_active = False
                    inv.save()
                    deleted = True
                    message = "El usuario (" + inv.email_invited + ") ya no podr&aacute; acceder a este grupo"
                    response = {"deleted": deleted, "message": message}
                else:  # no eliminar la invitacion
                    return HttpResponse(inv)
            except Exception:
                return HttpResponse(False)
    else:
        response = "Error invitacion"
    return HttpResponse(json.dumps(response), mimetype="application/json")


@login_required(login_url='/account/login')
def showMinutes(request, slug, minutes_id):
    group = groups.objects.get(slug=slug)
    minutes_current = minutes.objects.get(id_group=group, code=minutes_id)
    minutes_group = minutes.objects.filter(id_group=group.id)
    prev = None
    next = None
    try:
        prev = minutes.get_previous_by_date_created(minutes_current, id_group=group)
    except minutes.DoesNotExist:
        prev = False
    except Exception, e:
        print "prev: " + str(e)
    try:
        next = minutes.get_next_by_date_created(minutes_current, id_group=group)
    except minutes.DoesNotExist:
        next = False
    except Exception, e:
        print "next: " + str(e)
    members = rel_user_group.objects.filter(id_group=group, is_active=True)
    ctx = {"group": group, "minutes": minutes_current, "members": members,
            "minutes_list": minutes_group, "prev": prev, "next": next}
    return render_to_response('groups/showMinutes.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def newMinutes(request, slug):
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


@login_required(login_url='/account/login')
def newReunion(request, slug):
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
        else:
            form = newReunionForm()
        ctx = {'TITLE': "Actarium",
               "newReunionForm": form,
               }
        return render_to_response('groups/newReunion.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/groups/#error-view-group')


@login_required(login_url='/account/login')
def calendar(request):
    gr = groups.objects.filter(rel_user_group__id_user=request.user)  # grupos
    my_reu = reunions.objects.filter(id_group__in=gr, is_done=False)  # reuniones
    my_reu_day = reunions.objects.filter(id_group__in=gr)  # reuniones para un dia
    i = 0
    json_array = {}
    for reunion in my_reu_day:
        try:
            confirm = assistance.objects.get(id_user=request.user, id_reunion=reunion.pk)
            is_confirmed = confirm.is_confirmed
            is_saved = 1
        except assistance.DoesNotExist:
            is_confirmed = False
            is_saved = 0
        json_array[i] = {"id_r": str(reunion.id), "group_name": str(reunion.id_group.name), "date": (datetime.datetime.strftime(make_naive(reunion.date_reunion, get_default_timezone()), "%I:%M %p")), 'is_confirmed': str(is_confirmed), 'is_saved': is_saved}
        i = i + 1
    response = json_array
    ctx = {'TITLE': "Actarium",
       "reunions_day": my_reu,
       "reunions": my_reu,
       "my_reu_day_json": json.dumps(response)}
    return render_to_response('groups/calendar.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def calendarDate(request, slug=None):
    gr = groups.objects.filter(rel_user_group__id_user=request.user)  # grupos
    my_reu = reunions.objects.filter(id_group__in=gr, is_done=False)  # reuniones
    dateslug_min = str(make_aware(datetime.datetime.strptime(slug + " 00:00:00", '%Y-%m-%d %H:%M:%S'), get_default_timezone()))
    dateslug_max = str(make_aware(datetime.datetime.strptime(slug + " 23:59:59", '%Y-%m-%d %H:%M:%S'), get_default_timezone()))
    my_reu_day = reunions.objects.filter(id_group__in=gr, date_reunion__range=[dateslug_min, dateslug_max])  # reuniones para un dia
    i = 0
    json_array = {}
    for reunion in my_reu_day:
        try:
            confirm = assistance.objects.get(id_user=request.user, id_reunion=reunion.pk)
            is_confirmed = confirm.is_confirmed
            is_saved = 1
        except assistance.DoesNotExist:
            is_confirmed = False
            is_saved = 0
        json_array[i] = {"id_r": str(reunion.id), "group_name": str(reunion.id_group.name), "date": (datetime.datetime.strftime(make_naive(reunion.date_reunion, get_default_timezone()), "%I:%M %p")), 'is_confirmed': str(is_confirmed), 'is_saved': is_saved}
        i = i + 1
    response = json_array
    ctx = {'TITLE': "Actarium",
       "reunions_day": my_reu_day,
       "reunions": my_reu,
       "my_reu_day_json": json.dumps(response)}
    return render_to_response('groups/calendar.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def getReunions(request):
    if request.is_ajax():
        if request.method == 'GET':
            date = str(request.GET['date'])
            gr = groups.objects.filter(rel_user_group__id_user=request.user)  # grupos
            dateslug_min = str(make_aware(datetime.datetime.strptime(date + " 00:00:00", '%Y-%m-%d %H:%M:%S'), get_default_timezone()))
            dateslug_max = str(make_aware(datetime.datetime.strptime(date + " 23:59:59", '%Y-%m-%d %H:%M:%S'), get_default_timezone()))
            my_reu_day = reunions.objects.filter(id_group__in=gr, date_reunion__range=[dateslug_min, dateslug_max])  # reuniones para un dia
            i = 0
            json_array = {}
            for reunion in my_reu_day:
                try:
                    confirm = assistance.objects.get(id_user=request.user, id_reunion=reunion.pk)
                    is_confirmed = confirm.is_confirmed
                    is_saved = 1
                except assistance.DoesNotExist:
                    is_confirmed = False
                    is_saved = 0
                json_array[i] = {"id_r": str(reunion.id), "group_name": reunion.id_group.name, "date": (datetime.datetime.strftime(make_naive(reunion.date_reunion, get_default_timezone()), "%I:%M %p")), 'is_confirmed': is_confirmed, 'is_saved': is_saved}
                i = i + 1
            response = json_array
    else:
        response = "Error Calendar"
    return HttpResponse(json.dumps(response), mimetype="application/json")


def setAssistance(request):
    if request.is_ajax():
        if request.method == 'GET':
            id_reunion = reunions.objects.get(pk=request.GET['id_reunion'])
            id_user = request.user
            is_confirmed = str(request.GET['is_confirmed'])
            if (is_confirmed == "true"):
                is_confirmed = True
            else:
                is_confirmed = False
            assis, created = assistance.objects.get_or_create(id_user=id_user, id_reunion=id_reunion)
    #        if created:
    #            assis = assistance.objects.get(id_user=id_user, id_reunion=id_reunion)
            assis.is_confirmed = is_confirmed
    #        assis.is_confirmed = is_confirmed
            assis.save()
            print assis
            datos = "id_reunion = %s , id_user = %s , is_confirmed = %s, created %s" % (id_reunion.pk, id_user, is_confirmed, created)
            print datos
        return HttpResponse(json.dumps(datos), mimetype="application/json")
    else:
        response = "Error Calendar"
        return HttpResponse(json.dumps(response), mimetype="application/json")

def getReunionData(request):
    if request.is_ajax():
        if request.method == 'GET':
            id_reunion = str(request.GET['id_reunion'])
            reunion = reunions.objects.get(pk=id_reunion)
            convener = reunion.id_convener.username
            date_convened = reunion.date_convened
            date_reunion = reunion.date_reunion
            group = reunion.id_group.name
            id_group = reunion.id_group
            agenda = reunion.agenda
            is_done = reunion.is_done
            
            assistants = rel_user_group.objects.filter(id_group = id_group)
            assis_list = {}
            i = 0
            c = 0
            for assistant in assistants:
                try:
                    confirm = assistance.objects.get(id_user=assistant.id_user, id_reunion=reunion.pk)
                    is_confirmed = confirm.is_confirmed
                    is_saved = 1
                except assistance.DoesNotExist:
                    is_confirmed = False
                    is_saved = 0
                if( is_saved == 1):
                    if(is_confirmed == True): #reuniones confirmadas
                        c=1
                    else : #reuniones rechazadas
                        c=2
                else: #reuniones pendientes por confirmar
                    c=3
                
                assis_list[i] = {'username': assistant.id_user.username, "is_confirmed":c}
                i = i+1
            
            reunion_data = {"convener":convener,
               "date_convened": str(date_convened),
               "date_reunion": str(date_reunion),
               "group": group,
               "agenda": agenda, 
               "is_done": is_done,
               "assistants": assis_list           
           }
    else:
        reunion_data = "Error Calendar"
    return HttpResponse(json.dumps(reunion_data), mimetype="application/json")













