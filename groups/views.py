# Create your views here.
#encoding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import Http404
from groups.models import *
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
from Actarium.settings import URL_BASE
# import locale
# locale.setlocale(locale.LC_ALL, '')


@login_required(login_url='/account/login')
def groupsList(request):
    '''
    lista los grupos del usuario registrado
    '''
    try:
        mygroups = groups.objects.filter(rel_user_group__id_user=request.user, rel_user_group__is_active=True)
    except groups.DoesNotExist:
        mygroups = "Either the entry or blog doesn't exist."

    ctx = {'TITLE': "Actarium", "groups": mygroups}
    return render_to_response('groups/groupsList.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def groupSettings(request, slug_group):
    ctx = {}
    return render_to_response('groups/adminGroup.html', ctx, context_instance=RequestContext(request))


def setUserRoles(_user, _group, sadmin=False, is_admin=False, is_approver=False, is_secretary=False):
    try:
        relation = rel_user_group.objects.get(id_user=_user, id_group=_group)
        if sadmin:
            relation.is_superadmin = sadmin
        if is_admin:
            relation.is_admin = is_admin
        if is_secretary:
            relation.is_secretary = is_secretary
        if is_approver:
            relation.is_approver = is_approver
        relation.save()
    except rel_user_group.DoesNotExist:
        rel = rel_user_group(id_user=_user, id_group=_group,
        is_admin=is_admin, is_approver=is_approver, is_secretary=is_secretary, is_superadmin=sadmin)
        rel.save()


def get_user_or_email(s):
    if validateEmail(s):
        return {"user": False, "email": str(s)}
    else:
        try:
            if isinstance(int(s), int):  # valida si es un entero
                _user = User.objects.get(id=int(s))
                return {"user": _user, "email": str(s)}
        except User.DoesNotExist:
            return {"user": False, "email": str(s)}
        except Exception:
            return {"user": False, "email": False}


@login_required(login_url='/account/login')
def newFreeGroup(request, form):
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
    setUserRoles(request.user, myNewGroup, sadmin=True)
    user_or_email = get_user_or_email(request.POST['id_admin'])
    print user_or_email['user']
    if user_or_email['user']:
        setUserRoles(user_or_email['user'], myNewGroup, is_admin=True)
    admin_group(id_user=request.user, id_group=myNewGroup).save()
    saveActionLog(request.user, 'NEW_GROUP', "id_group: %s, group_name: %s, admin: %s" % (myNewGroup.pk, df['name'], request.user.username), request.META['REMOTE_ADDR'])  # Guardar accion de crear reunion
    # return HttpResponseRedirect("/groups/" + str(myNewGroup.slug))
    return myNewGroup


@login_required(login_url='/account/login')
def newProGroup(request, form):
    print "type-group: %s , id-organization: %s, id-billing: %s" % (request.POST['type-group'], request.POST['sel-organization'], request.POST['sel-billing'])
    try:
        org = organizations.objects.get(id=request.POST['sel-organization'], id_admin=request.user, is_active=True)
    except Exception, e:
        org = None
        raise e
    try:
        bill = billing.objects.get(id=request.POST['sel-billing'], id_user=request.user, state='1')
    except Exception, e:
        bill = None
        raise e
    if org and bill:
        # crear pro
        new_group = newFreeGroup(request, form)
        g_pro = groups_pro(id_group=new_group, id_organization=org, id_billing=bill)
        g_pro.save()
        return new_group
    else:
        return False


@login_required(login_url='/account/login')
def getProGroupDataForm(request):
    orgs = None
    billing_list = None
    try:
        orgs = organizations.objects.filter(is_active=True, id_admin=request.user)
    except Exception, e:
        orgs = None
        raise e
    try:
        billing_list = billing.objects.filter(state='1', id_user=request.user)
    except billing.DoesNotExist:
        billing_list = "No hay información disponible."
    return (orgs, billing_list)


@login_required(login_url='/account/login')
def newGroup(request):
    '''
        crea una nuevo grupo
    '''
    orgs = None
    billing_list = None
    sel_org = False
    if request.method == "GET":  # envia una variable para seleccionar una organizacion
        try:
            sel_org = request.GET['org']
        except Exception:
            sel_org = False

    if request.method == "POST":  # selecciona los datos para crear un nuevo grupo
        form = newGroupForm(request.POST)
        if form.is_valid():
            if int(request.POST['type-group']) == 0:  # 0 = grupo Free
                resp = newFreeGroup(request, form)
            else:
                resp = newProGroup(request, form)
            if resp:
                return HttpResponseRedirect("/groups/" + str(resp.slug))
    else:
        form = newGroupForm()
    orgs, billing_list = getProGroupDataForm(request)
    ctx = {"newGroupForm": form,
           "organizations": orgs,
           "billing": billing_list,
           "sel_org": sel_org
           }
    return render_to_response('groups/newGroup.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def showGroup(request, slug):
    '''
        Muestra la informacion de un grupo
    '''
    try:
        q = groups.objects.get(slug=slug, is_active=True)
    except groups.DoesNotExist:
        raise Http404
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
                        "user_id": ans.id,
                        "mail_is_valid": True,
                        "username": ans.username,
                        "mail": ans.email,
                        "gravatar": showgravatar(ans.email, 20)}
                else:
                    if ans == 1:
                        message = {"user_id": search, "mail_is_valid": True,
                                    "mail": search, "username": False,
                                    "gravatar": showgravatar(search, 20)}
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
                contenido = str(user.first_name.encode('utf8', 'replace')) + " (" + str(user.username.encode('utf8', 'replace')) + ") te ha invitado al grupo <strong>" + str(group.name.encode('utf8', 'replace')) + "</strong><br><br>" + "Ingresa a Actarium en: <a href='http://actarium.com' >Actarium.com</a> y acepta o rechaza &eacute;sta invitac&oacute;n."
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
                saveActionLog(request.user, 'SET_INVITA', "email: %s" % (mail), request.META['REMOTE_ADDR'])  # Accion de aceptar invitacion a grupo
                if inv and not inv is 0:
                    invited = True
                    iid = str(inv.id)
                    gravatar = showgravatar(mail, 30)
                    message = "Se ha enviado la invitación a " + str(mail) + " al grupo <strong>" + str(q.name) + "</strong>"
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
                    saveActionLog(request.user, 'SET_INVITA', "id_group: %s, acept: %s, group_name: %s" % (inv.id_group.pk, True, inv.id_group.name), request.META['REMOTE_ADDR'])  # Accion de aceptar invitacion a grupo
                    accepted = True
                    group = {"id": inv.id_group.id, "name": inv.id_group.name, "slug": "/groups/" + inv.id_group.slug, "img_group": inv.id_group.img_group}
                    message = "Aceptar la solicitud"
                else:  # no aprobar la invitacion
                    if inv and not accept:
                        inv.is_active = False
                        inv.save()
                        saveActionLog(request.user, 'SET_INVITA', "id_group: %s, acept: %s, group_name: %s" % (inv.id_group.pk, False, inv.id_group.name), request.META['REMOTE_ADDR'])  # Accion de aceptar invitacion a grupo
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
                    saveActionLog(request.user, 'DEL_INVITA', "id_invitacion: %s, grupo: %s, email_invited: %s" % (iid, inv.id_group.name, inv.email_invited), request.META['REMOTE_ADDR'])  # Accion de eliminar invitaciones
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
        members_signed = rel_user_minutes_assistance.objects.filter(id_minutes=minutes_current)
    except rel_user_minutes_assistance.DoesNotExist:
        members_signed = False
    except Exception, e:
        print "Error getMembersSigned: %s " % e
        members_signed = False
    return members_signed


def getMinutesById(minutes_id):
    try:
        the_minutes = minutes.objects.get(id=minutes_id)
    except minutes.DoesNotExist:
        the_minutes = False
    except Exception, e:
        print "Error getMinutesById: %s" % e
        the_minutes = False
    return the_minutes


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
        raise Http404
    except Exception, e:
        group = False
        raise Http404
        print "Error capturando grupo: %s " % e
    return group


def getMembersAssistance(group, minutes_current):
    try:
        selected = rel_user_minutes_assistance.objects.filter(id_minutes=minutes_current, assistance=True)
        no_selected = rel_user_minutes_assistance.objects.filter(id_minutes=minutes_current, assistance=False)
        return (selected, no_selected)
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

        ######## <ATTENDING> #########
        # try:
        #     my_attending = rel_user_minutes_assistance.objects.get(id_minutes=minutes_current, id_user=request.user)
        #     my_attending = my_attending.assistance
        # except Exception, e:
        #     print e
        #     my_attending = False
        ######## </ATTENDING> #########

        ######## <APPROVED LISTS> #########
        # missing_approved_list = rel_user_minutes_assistance.objects.filter(id_minutes=minutes_current, is_signed_approved=0)
        # missing_approved_list = 0 if len(missing_approved_list) == 0 else missing_approved_list
        # approved_list = rel_user_minutes_assistance.objects.filter(id_minutes=minutes_current, is_signed_approved=1)
        # approved_list = 0 if len(approved_list) == 0 else approved_list
        # no_approved_list = rel_user_minutes_assistance.objects.filter(id_minutes=minutes_current, is_signed_approved=2)
        # no_approved_list = 0 if len(no_approved_list) == 0 else no_approved_list
        ######## </APPROVED LISTS> #########

        ######## <PREV and NEXT> #########
        prev, next = getPrevNextOfGroup(group, minutes_current)
        ######## </PREV and NEXT> #########

        ctx = {"group": group, "minutes": minutes_current, "prev": prev, "next": next,
        "m_assistance": m_assistance, "m_no_assistance": m_no_assistance,
        # "my_attending": my_attending,
        # "missing_approved_list": missing_approved_list, "approved_list": approved_list, "no_approved_list": no_approved_list
        }
    else:
        return HttpResponseRedirect('/groups/#error-its-not-your-group')
    return render_to_response('groups/showMinutes.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def setApprove(request):
    if request.is_ajax():
        if request.method == 'GET':
            minutes_id = str(request.GET['m_id'])
            approved = 1 if int(request.GET['approve']) == 1 else 2
            try:
                sign = rel_user_minutes_assistance.objects.get(id_minutes=minutes_id, id_user=request.user)
                sign.is_signed_approved = approved
                sign.save()
            except Exception, e:
                print "Error Al Firmar" % e
            response = {"approved": approved, "minutes": minutes_id, "user-id": request.user.id, "user-name": request.user.first_name + " " + request.user.last_name}
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


def setMinuteAssistance(minutes_id, members_selected, members_no_selected):
    '''
    Stored in the database records all users attending a reunion.
    '''
    a = list()
    b = list()
    for m in members_selected:
        a.append(
            rel_user_minutes_assistance(
                id_user=m.id_user,
                id_minutes=minutes_id,
                assistance=True
                )
        )
    for m in members_no_selected:
        b.append(
            rel_user_minutes_assistance(
                id_user=m.id_user,
                id_minutes=minutes_id,
                assistance=False
                )
        )
    try:
        rel_user_minutes_assistance.objects.bulk_create(a)
        rel_user_minutes_assistance.objects.bulk_create(b)
    except Exception, e:
        print e
        return "Exception"


@login_required(login_url='/account/login')
def saveMinute(request, group, form, m_selected, m_no_selected):
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
                        id_type=minutes_type.objects.get(pk=1),  # pk=1 ==> Reunion
                    )
        myNewMinutes.save()
        id_user = request.user
        print "id_user: %s group: %s, code: %s" % (id_user, group.name, df['code'])
        saveActionLog(id_user, 'NEW_MINUTE', "group: %s, code: %s" % (group.name, df['code']), request.META['REMOTE_ADDR'])
        # registra los usuarios que asistieron a la reunión en la que se creó el acta
        setMinuteAssistance(myNewMinutes, m_selected, m_no_selected)
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


def getEmailListByGroup(group):
    '''
    Retorna los correos de los miembros activos de un grupo.
    '''
    try:
        group_list = rel_user_group.objects.filter(id_group=group, is_active=True)
        mails = list()
        for member in group_list:
            mails.append(member.id_user.email)
        return mails
    except Exception, e:
        print e


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
                save = saveMinute(request, group, form, m_selected, m_no_selected)
                if save:
                    saved = True
                    error = False
                    url_new_minute = "/groups/" + str(group.slug) + "/minutes/" + str(save.code)
                    link = URL_BASE + url_new_minute
                    email_list = getEmailListByGroup(group)
                    title = request.user.first_name + " (" + request.user.username + ") registro un acta en el grupo '" + str(group.name) + "' de Actarium"
                    content = request.user.first_name + " (" + request.user.username + ") ha creado una nueva acta en Actarium"
                    content = content + "<br><br>El link de la nueva Acta del grupo <strong>" + str(group.name) + "</strong> es: <a href='" + link + "'>" + link + "</a><br><br>"
                    content = content + "Ingresa a Actarium en: <a href='http://actarium.com' >Actarium.com</a><br>"
                    sendEmail(email_list, title, content)
                    return HttpResponseRedirect(url_new_minute)
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
                    form = newMinutesForm(initial={"agenda": reunion.agenda, "location": reunion.locale})
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
                    'title': form.cleaned_data['title'],
                    'locale': form.cleaned_data['locale'],
                    'agenda': form.cleaned_data['agenda'],
                }
                myNewReunion = reunions(
                               id_convener=request.user,
                               date_reunion=df['date_reunion'],
                               title=df['title'],
                               locale=df['locale'],
                               id_group=q,
                               agenda=df['agenda'],
                             )
                myNewReunion.save()
                relations = rel_user_group.objects.filter(id_group=q, is_active=1)
                email_list = []
                for relation in relations:
                    #print "Nombre %s Correo %s, fecha %s"%(relation.id_user.username,relation.id_user.email,  str(datetime.datetime.strftime(make_naive(df['date_reunion'], get_default_timezone()), "%Y-%m-%d %I:%M %p")))
                    email_list.append(str(relation.id_user.email) + ",")
                try:
                    title = str(request.user.first_name.encode('utf8', 'replace')) + " (" + str(request.user.username.encode('utf8', 'replace')) + ") Te ha invitado a una reunion del grupo " + str(q.name.encode('utf8', 'replace')) + " en Actarium"
                    contenido = "Reunion: <strong>" + str(df['title']) + "</strong><br><br>La reunion se programó para el d&iacute;a <strong>" + dateTimeFormatForm(df['date_reunion']) + "</strong> en <strong>" + str(df['locale']) + "</strong><br><br>Los objetivos propuestos por <strong>" + str(request.user.first_name.encode('utf8', 'replace')) + "</strong> son: <br><div style='color:gray'>" + str(df['agenda']) + "</div><br>" + "Ingresa a Actarium en: <a href='http://actarium.com' >Actarium.com</a><br>"
                    sendEmail(email_list, title, contenido)
                except Exception, e:
                    print "Exception mail: %s" % e

                id_reunion = reunions.objects.get(id_convener=request.user,
                               date_reunion=df['date_reunion'],
                               id_group=q,
                               agenda=df['agenda'])
                saveActionLog(request.user, 'NEW_REUNION', "Title: %s id_reunion: %s grupo: %s" % (str(df['title']), id_reunion.pk, q.name), request.META['REMOTE_ADDR'])  # Guardar accion de crear reunion
                return HttpResponseRedirect("/groups/calendar/" + str(datetime.datetime.strftime(make_naive(df['date_reunion'], get_default_timezone()), "%Y-%m-%d")) + "?r=" + str(id_reunion.pk))
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
    my_reu = reunions.objects.filter(id_group__in=gr, is_done=False).order_by("-date_convened")  # reuniones
    my_reu_day = reunions.objects.filter(id_group__in=gr).order_by("-date_convened")  # reuniones para un dia
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
        json_array[i] = {"id_r": str(reunion.id), "group_slug": str(reunion.id_group.slug), "group_name": str(reunion.id_group.name), "date": (datetime.datetime.strftime(make_naive(reunion.date_reunion, get_default_timezone()), "%d de %B de %Y a las %I:%M %p")), 'is_confirmed': str(is_confirmed), 'is_saved': is_saved, "title": reunion.title}
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
    my_reu = reunions.objects.filter(id_group__in=gr, is_done=False).order_by("-date_convened")  # reuniones
    dateslug_min = str(make_aware(datetime.datetime.strptime(slug + " 00:00:00", '%Y-%m-%d %H:%M:%S'), get_default_timezone()))
    dateslug_max = str(make_aware(datetime.datetime.strptime(slug + " 23:59:59", '%Y-%m-%d %H:%M:%S'), get_default_timezone()))
    my_reu_day = reunions.objects.filter(id_group__in=gr, date_reunion__range=[dateslug_min, dateslug_max]).order_by("-date_convened")  # reuniones para un dia
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
        json_array[i] = {"id_r": str(reunion.id), "group_slug": str(reunion.id_group.slug), "group_name": str(reunion.id_group.name), "date": (datetime.datetime.strftime(make_naive(reunion.date_reunion, get_default_timezone()), "%d de %B de %Y a las %I:%M %p")), 'is_confirmed': str(is_confirmed), 'is_saved': is_saved, 'title': reunion.title}
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
            my_reu_day = reunions.objects.filter(id_group__in=gr, date_reunion__range=[dateslug_min, dateslug_max]).order_by("-date_convened")  # reuniones para un dia
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
                json_array[i] = {"id_r": str(reunion.id), "group_slug": reunion.id_group.slug, "group_name": reunion.id_group.name, "date": (datetime.datetime.strftime(make_naive(reunion.date_reunion, get_default_timezone()), "%d de %B de %Y a las %I:%M %p")), 'is_confirmed': is_confirmed, 'is_saved': is_saved, "title": reunion.title}
                i = i + 1
            response = json_array
    else:
        response = "Error Calendar"
    return HttpResponse(json.dumps(response), mimetype="application/json")


@login_required(login_url='/account/login')
def getNextReunions(request):
    if request.is_ajax():
        gr = groups.objects.filter(rel_user_group__id_user=request.user)  # grupos
        my_reu_day = reunions.objects.filter(id_group__in=gr, date_reunion__gt=datetime.date.today()).order_by("date_reunion")  # reuniones para un dia
        i = 0
        json_array = {}
        for reunion in my_reu_day:
            if(i < 3):
                try:
                    confirm = assistance.objects.get(id_user=request.user, id_reunion=reunion.pk)
                    is_confirmed = confirm.is_confirmed
                    is_saved = 1
                    if (is_confirmed):
                        json_array[i] = {"id_r": str(reunion.id), "group_slug": reunion.id_group.slug, "group_name": reunion.id_group.name, "date": (datetime.datetime.strftime(make_naive(reunion.date_reunion, get_default_timezone()), "%d de %B de %Y a las %I:%M %p")), 'is_confirmed': is_confirmed, 'is_saved': is_saved, "title": reunion.title}
                        print "---------------------------------------------------------"
                        i = i + 1
                except assistance.DoesNotExist:
                    is_confirmed = False
                    is_saved = 0
        response = json_array
        print json_array
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


@login_required(login_url='/account/login')
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


@login_required(login_url='/account/login')
def getReunionData(request):
    if request.is_ajax():
        if request.method == 'GET':
            id_reunion = str(request.GET['id_reunion'])
            reunion = reunions.objects.get(pk=id_reunion)
            convener = reunion.id_convener.username
            date_convened = reunion.date_convened
            date_convened = removeGMT(date_convened)
            date_reunion = reunion.date_reunion
            date_reunion = removeGMT(date_reunion)
            locale = reunion.locale
            title = reunion.title
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
                        c = "Asistir&aacute;"
                    else:  # reuniones rechazadas
                        c = "No asistir&aacute;"
                else:  # reuniones pendientes por confirmar
                    c = "Sin responder"
                assis_list[i] = {'username': assistant.id_user.first_name + " (" + assistant.id_user.username + ")", "is_confirmed": c, "gravatar": showgravatar(assistant.id_user.email, 30)}
                i = i + 1
            iconf = 0
            try:
                my_confirm = assistance.objects.get(id_user=request.user, id_reunion=reunion.pk)
                my_confirmation = my_confirm.is_confirmed
                if my_confirmation == True:
                    iconf = 1
                else:
                    if my_confirmation == False:
                        iconf = 2
            except assistance.DoesNotExist:
                    iconf = 3
            reunion_data = {"convener": convener,
               "date_convened": str(dateTimeFormatDb(date_convened)),
               "date_reunion": str(dateTimeFormatDb(date_reunion)),
               "group": group,
               "agenda": agenda,
               "locale": locale,
               "title": title,
               "is_done": is_done,
               "assistants": assis_list,
               "group_slug": group_slug,
               "iconf": iconf
           }
    else:
        reunion_data = "Error Calendar"
    return HttpResponse(json.dumps(reunion_data), mimetype="application/json")


def dateTimeFormatForm(datetime_var):
    return str(datetime.datetime.strftime(make_naive(datetime_var, get_default_timezone()), "%d de %B de %Y a las %I:%M %p"))


def dateTimeFormatDb(datetime_var):
    UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now()
    local_datetime = datetime.datetime.strptime(str(datetime_var), "%Y-%m-%d %H:%M:%S")
    result_utc_datetime = local_datetime - UTC_OFFSET_TIMEDELTA
    return str(result_utc_datetime.strftime("%d de %B de %Y a las %I:%M %p"))


def removeGMT(datetime_var):
    dt = str(datetime_var)
    dt_s = dt[:19]
    return str(datetime.datetime.strptime("%s" % (dt_s), "%Y-%m-%d %H:%M:%S"))


def sendEmail(mail_to, titulo, contenido):
    contenido = contenido + "\n" + "<br><br><p style='color:gray'>Mensaje enviado por <a style='color:gray' href='http://daiech.com'>Daiech</a>. <br><br> Escribenos en twitter <a href='http://twitter.com/Actarium'>@Actarium</a> - <a href='http://twitter.com/Daiech'>@Daiech</a></p><br><br>"
    try:
        correo = EmailMessage(titulo, contenido, 'Actarium <no-reply@daiech.com>', mail_to)
        correo.content_subtype = "html"
        correo.send()
    except Exception, e:
        print e
