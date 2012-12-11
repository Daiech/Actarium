# Create your views here.
#encoding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from groups.models import groups, group_type, rel_user_group, minutes, invitations, minutes_type_1, minutes_type, reunions, admin_group, assistance, rel_user_minutes_signed
from groups.forms import newGroupForm, newMinutesForm, newReunionForm
from django.contrib.auth.models import User
#from django.core.mail import EmailMessage
import re
import datetime
from django.utils.timezone import make_aware, get_default_timezone, make_naive
from django.utils import simplejson as json
from account.templatetags.gravatartag import showgravatar
from django.core.mail import EmailMessage
from actions_log.views import saveActionLog


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
            saveActionLog(request.user, 'NEW_GROUP', "id_group: %s, group_name: %s, admin: %s" % (myNewGroup.pk, df['name'], request.user.username), request.META['REMOTE_ADDR'])  # Guardar accion de crear reunion
            #print "group: %s, id_group: %s"%(myNewGroup,myNewGroup.pk)
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
        email = [email]
        if created:
            try:
                title = str(user.first_name.encode('utf8', 'replace')) + " (" + str(user.username.encode('utf8', 'replace')) + ") te agrego a un grupo en Actarium"
                contenido = str(user.first_name.encode('utf8', 'replace')) + " (" + str(user.username.encode('utf8', 'replace')) + ") te ha invitado al grupo " + str(group.name.encode('utf8', 'replace')) + "\n\n" + "ingresa a Actarium en: <a href='http://actarium.daiech.com' >Actarium.com</a>"
                sendEmail(email, title, contenido)
            except Exception, e:
                print "Exception mail: %s" % e
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
        print "El usuario no existe: %s" % e
        return False
    except Exception, e:
        print "El usuario no existe, Exception: %s" % e
        return False


def isMemberOfGroupByEmail(email, id_group):
    if validateEmail(email):
        try:
            ans = User.objects.get(email=email)
        except User.DoesNotExist, e:
            print e
            return False
        except Exception, e:
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
            except Exception, e:
                print e
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
                    #print "user: %s, id_user: %s, id_group: %s, acept: %s, group_name: %s"%(request.user, request.user.pk, inv.id_group.pk, True, inv.id_group.name)
                    saveActionLog(request.user, 'SET_INVITA',"id_group: %s, acept: %s, group_name: %s"%(inv.id_group.pk, True, inv.id_group.name), request.META['REMOTE_ADDR']) # Accion de aceptar invitacion a grupo
                    accepted = True
                    group = {"id": inv.id_group.id, "name": inv.id_group.name, "slug": "/groups/" + inv.id_group.slug, "img_group": inv.id_group.img_group}
                    message = "Aceptar la solicitud"
                else:  # no aprobar la invitacion
                    if inv and not accept:
                        inv.is_active = False
                        inv.save()
                        saveActionLog(request.user, 'SET_INVITA',"id_group: %s, acept: %s, group_name: %s"%(inv.id_group.pk, False, inv.id_group.name), request.META['REMOTE_ADDR']) # Accion de aceptar invitacion a grupo
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
                    saveActionLog(request.user, 'DEL_INVITA',"id_invitacion: %s, grupo: %s, email_invited: %s"%(iid,inv.id_group.name, inv.email_invited), request.META['REMOTE_ADDR']) # Accion de eliminar invitaciones
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


def getMembersSigned(group, minutes_current):
    try:
        members_signed = rel_user_minutes_signed.objects.filter(id_minutes=minutes_current)
    except rel_user_minutes_signed.DoesNotExist:
        members_signed = False
    except Exception, e:
        print "Error getMembersSigned: %s " % e
        members_signed = False
    return members_signed


def getMinutesByCode(group, code_id):
    try:
        minutes_current = minutes.objects.get(id_group=group, code=code_id)
    except minutes.DoesNotExist:
        minutes_current = False
    except Exception, e:
        print "Error getMinutesByCode: %s" % e
        minutes_current = False
    return minutes_current


def getPrevNextOfGroup(group, minutes_id):
    prev = None
    next = None
    # print "GROUP: %s" % str(group)
    # print "MINUTES: %s" % str(minutes_id)
    try:
        prev = minutes.get_previous_by_date_created(minutes_id, id_group=group)
        # print "PREV: %s" % str(prev.code)
    except minutes.DoesNotExist:
        prev = False
    except Exception, e:
        print "Exception prev: " + str(e)
    try:
        next = minutes.get_next_by_date_created(minutes_id, id_group=group)
        # print "NEXT: %s" % str(next)
    except minutes.DoesNotExist:
        next = False
    except Exception, e:
        print "Exception next: " + str(e)
    return prev, next


def getGroupBySlug(slug):
    try:
        group = groups.objects.get(slug=slug)
    except groups.DoesNotExist:
        group = False
        print "El grupo no existe"
    except Exception, e:
        group = False
        print "Error capturando grupo: %s " % e
    return group


def getMembersAssistance(group, minutes_current):
    try:
        selected = rel_user_minutes_signed.objects.filter(id_minutes=minutes_current)
        s = list()
        for m in selected:
            s.append(int(m.id_user.id))
        return getMembersOfGroupWithSelected(group, s)
    except Exception, e:
        print e
        return None


@login_required(login_url='/account/login')
def showMinutes(request, slug, minutes_code):
    '''
    Muestra toda la informacion de un Acta (minutes)
    '''
    group = getGroupBySlug(slug)
    if not group:
        return HttpResponseRedirect('/groups/#error-there-is-not-the-group')

    if isMemberOfGroup(request.user, group):
        minutes_current = getMinutesByCode(group, minutes_code)
        if not minutes_current:
            return HttpResponseRedirect('/groups/' + slug + '/#error-there-is-not-that-minutes')

        ######## <ASISTENTES> #########
        m_assistance, m_no_assistance = getMembersAssistance(group, minutes_current)
        ######## <ASISTENTES> #########

        my_attending = False
        signed = {}
        for m in m_assistance:
            try:
                if m.id_user.id == request.user.id:
                    my_attending = True
                is_signed = rel_user_minutes_signed.objects.get(id_minutes=minutes_current, id_user=m.id_user)
                # print str(m.id_user) + " => " + str(is_signed.is_signed_approved)
                signed[int(m.id_user.id)] = int(is_signed.is_signed_approved)
            except Exception, e:
                print "Assistance Error: %s" % e
                is_signed = None
        ######## <SIGN> #########
        members_signed = getMembersSigned(group, minutes_current)
        ######## </SIGN> #########

        ######## <PREV and NEXT> #########
        prev, next = getPrevNextOfGroup(group, minutes_current)
        ######## </PREV and NEXT> #########

        ctx = {"group": group, "minutes": minutes_current, "my_attending": my_attending, "signed_list": signed,
        "members_signed": members_signed, "prev": prev, "next": next, "m_assistance": m_assistance, "m_no_assistance": m_no_assistance}
    else:
        return HttpResponseRedirect('/groups/#error-its-not-your-group')
    return render_to_response('groups/showMinutes.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def setSign(request):
    if request.is_ajax():
        if request.method == 'GET':
            minutes_id = str(request.GET['m_id'])
            response = {"minutes": minutes_id}
    else:
        response = "Error invitacion"
    return HttpResponse(json.dumps(response), mimetype="application/json")


def getMembersOfGroupWithSelected(group, select):
    '''
    return a tuple with the list of selected members and no selected members
    (selected_members, no_selected_members)
    the tuple is a rel_user_group object
    '''
    all_members = rel_user_group.objects.filter(id_group=group, is_active=True).order_by("id")
    memb_list = list()
    for m in all_members:
        memb_list.append(int(m.id_user.id))  # lista con id de todos los miembros del grupo
    # print memb_list
    selected_list = list()
    for l in select:
        selected_list.append(int(l))  # Lista de usuarios seleccionados
    # print selected_list
    no_selected_list = list(set(memb_list) - set(selected_list))  # lista de usuarios no seleccionados
    # print no_selected_list
    try:
        selected_members = rel_user_group.objects.filter(id_group=group, id_user__in=selected_list, is_active=True)
        no_selected_members = rel_user_group.objects.filter(id_group=group, id_user__in=no_selected_list, is_active=True)
    except rel_user_group.DoesNotExist:
        return None
    except Exception, e:
        raise e
        return None
    return (selected_members, no_selected_members)


def preparingToSign(members, minutes_id):
    '''
    Stored in the database records all users attending a reunion.
    '''
    a = list()
    for m in members:
        a.append(
            rel_user_minutes_signed(
                id_user=m.id_user,
                id_minutes=minutes_id
                )
        )
    try:
        rel_user_minutes_signed.objects.bulk_create(a)
    except Exception, e:
        print e
        return "Exception"


def saveMinute(request, group, form, m_selected):
    '''
    Save the minutes in the tables of data base: minutes_type_1, minutes
    return:
    '''
    df = {
    'code': form.cleaned_data['code'],
    'date_start': form.cleaned_data['date_start'],
    'date_end': form.cleaned_data['date_end'],
    'location': form.cleaned_data['location'],
    'agenda': form.cleaned_data['agenda'],
    'agreement': form.cleaned_data['agreement'],
    }
    try:
        minu = minutes.objects.get(id_group=group, code=form.cleaned_data['code'])
    except minutes.DoesNotExist, e:
        print e
        minu = None
    if minu == None:
        myNewMinutes_type_1 = minutes_type_1(
                       date_start=datetime.datetime.strptime(str(datetime.date.today()) + " " + str(df['date_start']), '%Y-%m-%d %H:%M:%S'),
                       date_end=datetime.datetime.strptime(str(datetime.date.today()) + " " + str(df['date_end']), '%Y-%m-%d %H:%M:%S'),
                       location=df['location'],
                       agenda=df['agenda'],
                       agreement=df['agreement'],
                     )
        myNewMinutes_type_1.save()
        myNewMinutes = minutes(
                        code=df['code'],
                        id_extra_minutes=myNewMinutes_type_1,
                        id_group=group,
                        id_type=minutes_type.objects.get(pk=1),
                    )
        myNewMinutes.save()
        id_user = request.user
        print "id_user: %s group: %s, code: %s"%(id_user, group.name, df['code'])
        saveActionLog(id_user,'NEW_MINUTE', "group: %s, code: %s"%(group.name, df['code']),request.META['REMOTE_ADDR'])
        # registra los usuarios que asistieron a la reunión en la que se creó el acta
        preparingToSign(m_selected, myNewMinutes)
        return myNewMinutes
    else:
        return False


def getLastMinutes(group):
    try:
        l = minutes.objects.filter(id_group=group).order_by("-date_created")[0]
        return l
    except Exception, e:
        print e
        return "---"


@login_required(login_url='/account/login')
def newMinutes(request, slug_group, id_reunion):
    '''
    This function creates a minutes with the form for this.
    '''
    reunion = None
    group = groups.objects.get(slug=slug_group, is_active=True)
    is_member = rel_user_group.objects.filter(id_group=group.id, id_user=request.user)
    if is_member:
        if request.method == "POST":
            form = newMinutesForm(request.POST)
            select = request.POST.getlist('members[]')
            m_selected, m_no_selected = getMembersOfGroupWithSelected(group.id, select)
            if form.is_valid() and len(select) != 0:
                save = saveMinute(request, group, form, m_selected)
                if save:
                    saved = True
                    error = False
                    return HttpResponseRedirect("/groups/" + str(group.slug) + "/minutes/" + str(save.code))
                else:
                    saved = False
                    error = "e2"  # error, mismo código de acta, o error al guardar en la db
            else:
                saved = False
                error = "e0"  # error, el formulario no es valido
                if len(select) == 0:
                    error = "e1"  # error, al menos un (1) miembro debe ser seleccionado
        else:
            saved = False
            error = False
            if id_reunion:
                try:
                    reunion = reunions.objects.get(id=id_reunion)
                    print reunion.agenda
                    form = newMinutesForm(initial={"agenda": reunion.agenda})
                    print form
                    form.code = 123
                    confirm = assistance.objects.filter(id_reunion=reunion.pk, is_confirmed=True)
                    reunion_list = []  # Lista de miembros que confirmaron la asistencia
                    for user_confirmed in confirm:
                        reunion_list.append(int(user_confirmed.id_user.id))
                    m_selected, m_no_selected = getMembersOfGroupWithSelected(group.id, reunion_list)
                except reunions.DoesNotExist:
                    reunion = None
                except Exception, e:
                    reunion = None
                    m_selected = None
                    m_no_selected = None
                    error = "e3"
                    print "Exception newReunion: %s" % e
            else:
                form = newMinutesForm(initial={"agenda": "<ol><li>Lectura del Acta anterior</li></ol>"})
                reunion = None
                try:
                    m_selected = rel_user_group.objects.filter(id_group=group.id, is_active=True)
                    m_no_selected = None
                except rel_user_group.DoesNotExist:
                    m_selected = None
                except Exception, e:
                    print "Exception members in newMinutes: %e" % e
        last = getLastMinutes(group)
        ctx = {'TITLE': "Actarium - Nueva Acta",
               "newMinutesForm": form,
               "group": group,
               "reunion": reunion,
               "members_selected": m_selected,
               "members_no_selected": m_no_selected,
               "minutes_saved": {"saved": saved, "error": error},
               "last": last
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
                               id_convener=request.user,
                               date_reunion=df['date_reunion'],
                               id_group=q,
                               agenda=df['agenda'],
                             )
                myNewReunion.save()
                relations = rel_user_group.objects.filter(id_group= q, is_active=1)
                email_list = []
                for relation in relations:
                    #print "Nombre %s Correo %s, fecha %s"%(relation.id_user.username,relation.id_user.email,  str(datetime.datetime.strftime(make_naive(df['date_reunion'], get_default_timezone()), "%Y-%m-%d %I:%M %p")))
                    email_list.append(str(relation.id_user.email)+",")
                try:
                    title = str(request.user.first_name.encode('utf8', 'replace')) + " (" + str(request.user.username.encode('utf8', 'replace')) + ") Te ha invitado a una reunion en Actarium"
                    contenido = "La reunion se programó para la siguiente fecha y hora: " + str(datetime.datetime.strftime(make_naive(df['date_reunion'], get_default_timezone()), "%Y-%m-%d %I:%M %p")) + "\n\n\n" + "<br><br>Objetivos: \n\n"+ str(df['agenda'])+"\n\n" + "ingresa a Actarium en: <a href='http://actarium.daiech.com' >Actarium.com</a>"
                    sendEmail(email_list, title, contenido)
                except Exception, e:
                    print "Exception mail: %s" % e
                    
                id_reunion = reunions.objects.get(id_convener=request.user,
                               date_reunion=df['date_reunion'],
                               id_group=q,
                               agenda=df['agenda'])
                saveActionLog(request.user, 'NEW_REUNION',"id_reunion: %s grupo: %s"%(id_reunion.pk, q.name), request.META['REMOTE_ADDR']) #Guardar accion de crear reunion
                return HttpResponseRedirect("/groups/calendar/" +  str(datetime.datetime.strftime(make_naive(df['date_reunion'], get_default_timezone()), "%Y-%m-%d"))+"?r="+str(id_reunion.pk))
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
        json_array[i] = {"id_r": str(reunion.id),"group_slug": str(reunion.id_group.slug), "group_name": str(reunion.id_group.name), "date": (datetime.datetime.strftime(make_naive(reunion.date_reunion, get_default_timezone()), "%I:%M %p")), 'is_confirmed': str(is_confirmed), 'is_saved': is_saved}
        i = i + 1
    response = json_array
    ctx = {'TITLE': "Actarium",
       "reunions_day": my_reu,
       "reunions": my_reu,
       "my_reu_day_json": json.dumps(response),
       "groups": gr}
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
        json_array[i] = {"id_r": str(reunion.id),"group_slug": str(reunion.id_group.slug), "group_name": str(reunion.id_group.name), "date": (datetime.datetime.strftime(make_naive(reunion.date_reunion, get_default_timezone()), "%I:%M %p")), 'is_confirmed': str(is_confirmed), 'is_saved': is_saved}
        i = i + 1
    response = json_array
    ctx = {'TITLE': "Actarium",
       "reunions_day": my_reu_day,
       "reunions": my_reu,
       "my_reu_day_json": json.dumps(response),
       "groups": gr}
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
                json_array[i] = {"id_r": str(reunion.id),"group_slug": reunion.id_group.slug ,"group_name": reunion.id_group.name, "date": (datetime.datetime.strftime(make_naive(reunion.date_reunion, get_default_timezone()), "%I:%M %p")), 'is_confirmed': is_confirmed, 'is_saved': is_saved}
                i = i + 1
            response = json_array
    else:
        response = "Error Calendar"
    return HttpResponse(json.dumps(response), mimetype="application/json")


def getAssistance(id_minutes):
    try:
        assistan = assistance.objects.filter(id_minutes=id_minutes)
    except Exception, e:
        raise e
        assistan = False
    return assistan


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
            saveActionLog(id_user, 'SET_ASSIST', "id_reunion: %s, is_confirmed: %s" % (id_reunion.pk, is_confirmed), request.META['REMOTE_ADDR'])
            #print assis
            #print request.META['REMOTE_ADDR']
            datos = "id_reunion = %s , id_user = %s , is_confirmed = %s, created %s" % (id_reunion.pk, id_user, is_confirmed, created)
           # print datos
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
            group_slug = reunion.id_group.slug
            assistants = rel_user_group.objects.filter(id_group=id_group)
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
                if is_saved == 1:
                    if is_confirmed == True:  # reuniones confirmadas
                        c = "Asistirá"
                    else:  # reuniones rechazadas
                        c = "No asistirá"
                else:  # reuniones pendientes por confirmar
                    c = "Sin responder"
                assis_list[i] = {'username': assistant.id_user.username, "is_confirmed": c}
                i = i + 1
            iconf = 0;
            try:
                my_confirm = assistance.objects.get(id_user=request.user, id_reunion=reunion.pk)
                my_confirmation = my_confirm.is_confirmed
                if my_confirmation == True:
                    iconf= 1
                else:
                    if my_confirmation == False:
                        iconf= 2
            except assistance.DoesNotExist:
                    iconf= 3
            reunion_data = {"convener": convener,
               "date_convened": str(date_convened),
               "date_reunion": str(date_reunion),
               "group": group,
               "agenda": agenda,
               "is_done": is_done,
               "assistants": assis_list,
               "group_slug": group_slug,
               "iconf": iconf
           }
    else:
        reunion_data = "Error Calendar"
    return HttpResponse(json.dumps(reunion_data), mimetype="application/json")


def sendEmail(mail_to, titulo, contenido):
    contenido = contenido + "\n" + "<br><br><p style='color:gray'>Mensaje enviado por Daiech. <br><br> Escribenos en twitter <a href='http://twitter.com/Actarium'>@Actarium</a>, <a href='http://twitter.com/Daiech'>@Daiech</a></p><br><br>"
    try:
        correo = EmailMessage(titulo, contenido, 'Actarium <no-reply@daiech.com>', mail_to)
        correo.content_subtype = "html"
        correo.send()
    except Exception, e:
        print e
