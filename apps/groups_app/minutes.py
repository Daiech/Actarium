#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
import json
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

# imports from application
from apps.groups_app.models import *
from apps.groups_app.forms import newMinutesForm
from Actarium.settings import URL_BASE, MEDIA_URL
from apps.account.templatetags.gravatartag import showgravatar

# Imports from views.py
from apps.groups_app.views import getGroupBySlug, isMemberOfGroup, getRelUserGroup, get_user_or_email
from .utils_meetings import date_time_format_form, date_time_format_db, remove_gmt
from .utils import send_email_full_signed, getEmailListByGroup
from apps.actions_log.views import saveActionLog, saveViewsLog
# from Actarium.settings import URL_BASE
from apps.emailmodule.views import sendEmailHtml
from actarium_apps.organizations.models import rel_user_group


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
        return minutes.objects.get(id_group=group, code=code_id)
    except minutes.DoesNotExist:
        return None
    except Exception, e:
        print "Error getMinutesByCode: %s" % e
        return None


def getPrevNextOfGroup(group, minutes_id):
    prev = None
    next = None
    try:
        prev = minutes.get_previous_by_date_created(minutes_id, id_group=group)
    except minutes.DoesNotExist:
        prev = False
    except Exception, e:
        print "Exception prev: " + str(e)
    try:
        next = minutes.get_next_by_date_created(minutes_id, id_group=group)
    except minutes.DoesNotExist:
        next = False
    except Exception, e:
        print "Exception next: " + str(e)
    return prev, next


def getRolUserMinutes(_user, id_group, id_minutes=None):
    try:
        return rol_user_minutes.objects.get(id_user=_user, id_group=id_group, id_minutes=id_minutes)
    except rol_user_minutes.DoesNotExist:
        return None
    except Exception, e:
        print "getRolUserMinutes Error", e
        return None


def getMembersSigned(group, minutes_current):  # not called
    try:
        members_signed = rel_user_minutes_assistance.objects.filter(id_minutes=minutes_current)
    except rel_user_minutes_assistance.DoesNotExist:
        members_signed = False
    except Exception, e:
        print "Error getMembersSigned: %s " % e
        members_signed = False
    return members_signed


def getMembersAssistance(group, minutes_current):
    try:
        selected = rel_user_minutes_assistance.objects.filter(id_minutes=minutes_current, assistance=True)
        no_selected = rel_user_minutes_assistance.objects.filter(id_minutes=minutes_current, assistance=False)
        return (selected, no_selected)
    except Exception, e:
        print e
        return None


def getMembersSigners(group, minutes_current):
    try:
        selected = rol_user_minutes.objects.filter(id_group=group, is_signer=True, is_secretary=False, is_president=False, id_minutes=minutes_current)
        return selected
    except Exception, e:
        print e
        return None


def getAssistanceFromRolUserMinutes(group, id_minutes=None):
    try:
        if id_minutes:
            selected = rol_user_minutes.objects.filter(id_group=group, id_minutes=id_minutes, is_assistant=True, is_active=True)
        else:
            selected = rol_user_minutes.objects.filter(id_group=group, is_assistant=True, is_active=False)
        a = list()
        for m in selected:
            a.append(m.id_user.id)
        return getMembersOfGroupWithSelected(group, a)
    except Exception, e:
        print e
        return None


def getSignersFromRolUserMinutes(group, id_minutes=None):
    try:
        if id_minutes:
            selected = rol_user_minutes.objects.filter(id_group=group, id_minutes=id_minutes, is_active=True, is_signer=True, is_secretary=False, is_president=False)
        else:
            selected = rol_user_minutes.objects.filter(id_group=group, is_active=False, is_signer=True, is_secretary=False, is_president=False)
        return selected
    except Exception, e:
        print e
        return None


def getMembersOfGroupWithSelected(group, select):
    '''
    return a tuple with the list of selected members and no selected members
    (selected_members, no_selected_members)
    the tuple is a rel_user_group object
    '''
    all_members = rel_user_group.objects.filter(id_group=group, is_member=True).order_by("id")
    memb_list = list()
    for m in all_members:
        memb_list.append(int(m.id_user.id))  # lista con id de todos los miembros del grupo
    # print "Todos:", memb_list
    selected_list = list()
    for l in select:
        selected_list.append(int(l))  # Lista de usuarios seleccionados
    # print "selected_list:", selected_list
    no_selected_list = list(set(memb_list) - set(selected_list))  # lista de usuarios no seleccionados
    # print "no_selected_list:", no_selected_list
    try:
        selected_members = rel_user_group.objects.filter(id_group=group, id_user__in=selected_list, is_member=True)
        no_selected_members = rel_user_group.objects.filter(id_group=group, id_user__in=no_selected_list, is_member=True)
        # print "selected_members:", selected_members
        # print "no_selected_members:", no_selected_members
    except rel_user_group.DoesNotExist:
        return None
    except Exception:
        return None
    return (selected_members, no_selected_members)


def getLastMinutes(group):
    try:
        l = minutes.objects.filter(id_group=group).order_by("-date_created")[0]
        return l
    except Exception, e:
        print e
        return "---"


def getRelUserMinutesSigned(_user, _minutes):
    try:
        return rel_user_minutes_signed.objects.get(id_user=_user, id_minutes=_minutes)
    except rel_user_minutes_signed.DoesNotExist:
        return None
    except Exception, e:
        print "getRelUserMinutesSigned:", e
        return False


def getAllMinutesSigned(_minutes):
    try:
        return rel_user_minutes_signed.objects.filter(id_minutes=_minutes)
    except rel_user_minutes_signed.DoesNotExist:
        return None
    except Exception, e:
        print "ERROR minutes.getAllMinutesSigned:", e
        return False


def getRelUserMinutesAssistance(id_minutes, id_user):
    try:
        return rel_user_minutes_assistance.objects.get(id_minutes=id_minutes, id_user=id_user)
    except rel_user_minutes_assistance.DoesNotExist:
        return None
    except Exception, e:
        print "ERROR minutes.getRelUserMinutesAssistance:", e
        return None


def getReunionById(id_reunion):
    try:
        _reunion = reunions.objects.get(id=id_reunion)  # esta reunion pertenece a un grupo mio?
        if _reunion:
            if _reunion.hasMinutes():
                return False
            return _reunion
    except reunions.DoesNotExist:
        return None
    except Exception:
        return None


def getTemplateMinutes(slug_template):
    try:
        _template = templates.objects.get(slug=str(slug_template))
    except templates.DoesNotExist:
        _template = templates.objects.get(id=1)
    return _template


def getAllPrivateTemplates(id_group=None, id_user=False):
    try:
        if id_group:
            return private_templates.objects.filter(id_group=id_group)
        if id_user:
            return private_templates.objects.filter(id_user=id_user)
    except Exception:
        return None
    return None


def getAllPublicTemplates():
    try:
        return templates.objects.filter(is_public=True)
    except Exception:
        return None


def removeUniqueRolGroup(group, role):
    try:
        if role == 4:
            r = rol_user_minutes.objects.get(id_group=group, is_president=True, is_active=False)
            r.is_president = False
            # r.is_signer = False
        if role == 5:
            r = rol_user_minutes.objects.get(id_group=group, is_secretary=True, is_active=False)
            r.is_secretary = False
            # r.is_signer = False
        r.save()
        return True
    except rol_user_minutes.DoesNotExist:
        return True
    except Exception:
        return False


def updateRolUserMinutes(request, group, _minute, for_approvers=False):
    saveViewsLog(request, "apps.groups_app.minutes.updateRolUserMinutes")
    try:
        rols = rol_user_minutes.objects.filter(id_group=group, is_active=False)

        email_list = list()
        for r in rols:
            if r.is_approver:
                email_list.append(r.id_user.email)
                # print "SET:", setRelUserMinutesSigned(r.id_user, _minute, 0)

        rols.update(is_active=True, id_minutes=_minute)
    except Exception, e:
        print "newMinutes Error", e
        # saveErrorLog
    url_new_minute = "/groups/" + str(group.slug) + "/minutes/" + str(_minute.code)
    url_new_minute = reverse("show_minute", args=(group.slug, _minute.code))
    link = URL_BASE + url_new_minute

    email_ctx = {
        'code':_minute.code,
        'firstname': request.user.first_name,
        'username': request.user.username,
        'groupname': group.name,
        'link': link,
        'urlgravatar': showgravatar(request.user.email, 50)
    }
    if for_approvers:
        sendEmailHtml(13, email_ctx, email_list)
    # else:
    #     sendEmailHtml(3, email_ctx, getEmailListByGroup(group))
    return url_new_minute


def setRolUserMinutes(id_user, id_group, id_minutes=None, is_president=False,
    is_approver=False, is_secretary=False, is_assistant=False, is_signer=False, is_active=False):
    try:
        rel = rol_user_minutes(
            id_user=id_user,
            id_group=id_group,
            id_minutes=id_minutes,
            is_president=is_president,
            is_approver=is_approver,
            is_secretary=is_secretary,
            is_assistant=is_assistant,
            is_signer=is_signer,
            is_active=is_active)
        rel.save()
        # saveAction new Rol user minutes
        return True
    except Exception, e:
        print "erroooor:", e
        # error log
        return False


def setRelUserMinutesSigned(_user, _minutes, is_signed_approved):
    try:
        rel_user_minutes_signed.objects.get(id_user=_user, id_minutes=_minutes, is_signed_approved=is_signed_approved)
        return "Ya hay un registro"
    except rel_user_minutes_signed.DoesNotExist:
        rel_user_minutes_signed(id_user=_user, id_minutes=_minutes, is_signed_approved=is_signed_approved).save()
        return True
    except Exception, e:
        print "SetRelUserMinutesSigned:", e
        return False


def setMinuteAssistance(minutes_id, members_selected, members_no_selected):  # not called
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
                assistance=True)
        )
    for m in members_no_selected:
        b.append(
            rel_user_minutes_assistance(
                id_user=m.id_user,
                id_minutes=minutes_id,
                assistance=False)
        )
    try:
        rel_user_minutes_assistance.objects.bulk_create(a)
        rel_user_minutes_assistance.objects.bulk_create(b)
    except Exception, e:
        print "Minutes.setMinuteAssistance", e
        return False


def setRelationReunionMinutes(_reunion, _minute):
    try:
        rel_reunion_minutes(id_reunion=_reunion, id_minutes=_minute).save()
        return True
    except Exception:
        return False


@login_required(login_url='/account/login')
def setMinutesApprove(request):
    saveViewsLog(request, "apps.groups_app.minutes.setMinutesApprove")
    if request.is_ajax():
        if request.method == 'POST':
            try:
                minutes_id = str(request.POST.get('m_id'))
                approved = 1 if int(request.POST.get('approve')) == 1 else 2
                _minutes = getMinutesById(minutes_id)
                sign = getRelUserMinutesSigned(request.user, _minutes)
                if sign.is_signed_approved == 0:
                    sign.is_signed_approved = approved
                    sign.save()
                signs = getAllMinutesSigned(_minutes)
                is_full_signed = 1
                for s in signs:
                    if s.is_signed_approved == 0:
                        is_full_signed = 0
                if is_full_signed == 1:
                    _minutes.set_full_signed()
                    send_email_full_signed(_minutes)
            except Exception, e:
                print "Error Al aprobar: %s" % e
            response = {"approved": approved, "minutes": minutes_id,
            "user-id": request.user.id, "is_full_signed": _minutes.is_full_signed,
            "user-name": request.user.first_name + " " + request.user.last_name}
    else:
        response = "Error invitacion"
    return HttpResponse(json.dumps(response), mimetype="application/json")


def getLastMinutesAnnotation(id_minutes):
    try:
        a = annotations.objects.filter(id_minutes=id_minutes).order_by("-date_joined")[0]
        return a.id_minutes_annotation
    except annotations.DoesNotExist:
        return 0
    except Exception:
        return 0


def getApproversFromMinutes(id_minutes):
    try:
        return rol_user_minutes.objects.filter(id_minutes=id_minutes, is_approver=True, is_active=True)
    except rol_user_minutes.DoesNotExist:
        return None
    except Exception, e:
        print "ERROR getApproversFromMinutes", e
        return None


def getWritersOfGroup(id_group):
    try:
        return rel_user_group.objects.filter(id_group=id_group, is_secretary=True, is_active=True)
    except rel_user_group.DoesNotExist:
        return None
    except Exception, e:
        print "ERROR getWritersOfGroup", e
        return None


def getPresidentAndSecretary(group, minutes_current=None):
    if minutes_current:
        try:
            member_president = rol_user_minutes.objects.get(id_group=group, id_minutes=minutes_current, is_president=True)
        except Exception, e:
            print "ERROR no hay presidente", e
            member_president = None
        try:
            member_secretary = rol_user_minutes.objects.get(id_group=group, id_minutes=minutes_current, is_secretary=True)
        except Exception, e:
            print "ERROR no hay Secretario", e
            member_secretary = None
    else:
        try:
            member_president = rol_user_minutes.objects.get(id_group=group, is_active=False, is_president=True)
        except Exception, e:
            print "ERROR no hay presidente", e
            member_president = None
        try:
            member_secretary = rol_user_minutes.objects.get(id_group=group, is_active=False, is_secretary=True)
        except Exception, e:
            print "ERROR no hay Secretario", e
            member_secretary = None
    return (member_president, member_secretary)


def newAnnotation(request, slug_group):
    saveViewsLog(request, "apps.groups_app.minutes.newAnnotation")
    if request.is_ajax():
        if request.method == 'POST':
            try:
                g = getGroupBySlug(slug_group)
                annon_text = request.POST['annotation']
                minutes_id = getMinutesById(request.POST['minutes_id'])
                if minutes_id.id_group == g:
                    last_annon = getLastMinutesAnnotation(minutes_id)
                    annon = annotations(id_user=request.user, id_minutes=minutes_id, annotation_text=annon_text, id_minutes_annotation=last_annon + 1)
                    annon.save()
                    # saveActionLog
                    # sendEmail to the approvers # investigar sobre hilos en python para retornarle al usuario y quedarse enviando los correos (celery)

                    writter_group = getWritersOfGroup(g)
                    approver_list = getApproversFromMinutes(minutes_id)
                    email_list = list()
                    for ap in writter_group:
                        email_list.append(ap.id_user.email)
                    email_list = list()
                    for ap in approver_list:
                        email_list.append(ap.id_user.email)
                   # send Email HERE with email_list, annon, g. In annon var is all information. See  https://www.lucidchart.com/documents/edit/4853-1dd4-506e2365-bf06-76620ad6e19c
                    ctx_email = {
                        "firstname": request.user.first_name,
                        "username": request.user.username,
                        "groupname": g.name,
                        "minutes_code": annon.id_minutes.code,
                        "link": reverse("show_minute", args=(g.slug, annon.id_minutes.code,)) + "#annotation-" + str(annon.id_minutes_annotation),
                        "annotation": annon.annotation_text,
                        "urlgravatar": showgravatar(request.user.email, 50)
                    }
                    sendEmailHtml(12, ctx_email, email_list)
                    response = {"data": "success, send a socket to say them to the other connected"}
                else:
                    print "else"
            except Exception, e:
                print "ERROR newAnnotation", e
                response = {"error": "Error"}
        else:
            response = {"error": "Debe ser GET"}
    else:
        response = {"error": int(request.GET['minutes_id'])}
    return HttpResponse(json.dumps(response), mimetype="application/json")


@login_required(login_url='/account/login')
def setRolForMinute(request, slug_group):
    """
        Set or remove role to a user
        Roles id:
            1 = Signer
            2 = Approver
            3 = Assistance
            4 = President
            5 = Secretary
    """
    saveViewsLog(request, "apps.groups_app.minutes.setRolForMinute")
    r1, r2, r3, r4, r5 = "Firmador", "Aprobador", "Asistente", "Presidente", "Secretario"
    error = None
    saved = True
    role_name = ""
    if request.is_ajax():
        if request.method == 'GET':
            try:
                g = getGroupBySlug(slug=slug_group)
                _user_rel = getRelUserGroup(request.user, g)

                if _user_rel.is_secretary:
                    role = int(request.GET['role'])
                    remove = bool(int(request.GET['remove']))
                    _user = get_user_or_email(request.GET['uid'])
                    u = _user['user']
                    if u:
                        rel = getRolUserMinutes(u, g)
                    if not rel:
                        rel = setRolUserMinutes(u, g)
                        if rel:
                            rel = getRolUserMinutes(u, g)
                        else:
                            rel = False
                    if rel:
                        if role == 1 and u and not remove:
                            rel.is_signer = True
                            role_name = r1
                        if role == 2 and u and not remove:
                            rel.is_approver = True
                            role_name = r2
                        if role == 3 and u and not remove:
                            rel.is_assistant = True
                            role_name = r3
                        if role == 4 and u and not remove:
                            if removeUniqueRolGroup(g, 4):
                                if not rel.is_secretary:
                                    rel.is_president = True
                                else:
                                    error = "No se puede ser Secretario y Presidente al mismo tiempo"
                            role_name = r4
                        if role == 5 and u and not remove:
                            if removeUniqueRolGroup(g, 5):
                                if not rel.is_president:
                                    rel.is_secretary = True
                                else:
                                    error = "No se puede ser Presidente y Secretario al mismo tiempo"
                            role_name = r5

                        if role == 1 and u and remove:
                            rel.is_signer = False
                        if role == 2 and u and remove:
                            rel.is_approver = False
                        if role == 3 and u and remove:
                            rel.is_assistant = False
                        rel.save()
                        saved = True
                        # saveAction added Rol: group: g, user: u, role = role, role name=role_name, set or remove?: remove
                else:
                    error = "No tienes permiso para hacer eso, Por favor recarga la p&aacute;gina"
            except Groups.DoesNotExist:
                error = "Este grupo no existe"
            except rol_user_minutes.DoesNotExist:
                error = "Error! no existe el usuario para esta acta"
            except Exception, e:
                print "OCURRIO UN ERROR AL AGREGAR UN ROL:", e
                error = "Por favor recarga la p&aacute;gina e intenta de nuevo."
            if error:
                return HttpResponse(json.dumps({"error": error, "saved": False}), mimetype="application/json")
            response = {"saved": saved, "u": u.first_name, "role": role_name, "uid": u.id}
            return HttpResponse(json.dumps(response), mimetype="application/json")
    return HttpResponse(json.dumps({"error": "You can not enter here"}), mimetype="application/json")


@login_required(login_url='/account/login')
def setShowDNI(request, slug_group):
    """
        Ajax to set show-dni on table rel_group_dni
    """
    saveViewsLog(request, "apps.groups_app.minutes.setShowDNI")
    error = None
    saved = True
    if request.is_ajax():
        if request.method == 'GET':
            try:
                g = getGroupBySlug(slug=slug_group)
                _user_rel = getRelUserGroup(request.user, g)

                if _user_rel.is_secretary:
                    try:
                        rel = rel_group_dni.objects.get(id_group=g)
                        s_dni = rel.show_dni
                        if s_dni:
                            rel.show_dni = False
                        else:
                            rel.show_dni = True
                    except rel_group_dni.DoesNotExist:
                        rel = rel_group_dni(id_group=g, id_admin=request.user, show_dni=True)
                    rel.save()
                    saved = True
                else:
                    error = "No tienes permiso para hacer eso, Por favor recarga la p&aacute;gina"
            except Groups.DoesNotExist:
                error = "Este grupo no existe"
            except rol_user_minutes.DoesNotExist:
                error = "Error! no existe el usuario para esta acta"
            except Exception:
                error = "Por favor recarga la p&aacute;gina e intenta de nuevo."
            if error:
                return HttpResponse(json.dumps({"error": error, "saved": False}), mimetype="application/json")
            response = {"saved": saved}
            return HttpResponse(json.dumps(response), mimetype="application/json")
    return HttpResponse(json.dumps({"error": "You can not enter here"}), mimetype="application/json")


@login_required(login_url='/account/login')
def rolesForMinutes(request, slug_group, id_reunion=None):
    '''
    return the board to set the roles for a new Minutes
    '''
    saveViewsLog(request, "apps.groups_app.minutes.rolesForMinutes")
    try:
        if id_reunion:
            reunion = reunions.objects.get(id=id_reunion).id
        else:
            reunion = ""
    except reunions.DoesNotExist:
        reunion = ""
    g = getGroupBySlug(slug_group)
    _user_rel = getRelUserGroup(request.user, g.id)
    if _user_rel.is_secretary and _user_rel.is_active:
        members = rel_user_group.objects.filter(id_group=g, is_member=True).order_by("-is_active")
        _members = list()
        for m in members:
            try:
                rel = rol_user_minutes.objects.get(id_group=g, id_user=m.id_user, id_minutes=None, is_active=False)
            except rol_user_minutes.DoesNotExist:
                rel = None
            _members.append({"member": m, "rol": rel})
            try:
                _secretary = rol_user_minutes.objects.get(id_group=g, is_active=False, is_secretary=True).id_user.id
            except rol_user_minutes.DoesNotExist:
                _secretary = None
            except Exception:
                _secretary = None
            try:
                _president = rol_user_minutes.objects.get(id_group=g, is_active=False, is_president=True).id_user.id
            except rol_user_minutes.DoesNotExist:
                _president = None
            except Exception:
                _president = None
        # get last template used
        try:
            template = minutes.objects.filter(id_group=g, is_valid=True).order_by("-code")[0]
            template = template.id_template.slug
        except Exception:
            template = ""
        try:
            rel = rel_group_dni.objects.get(id_group=g)
            if rel.show_dni == True:
                show_dni = True
            else:
                show_dni = False
        except rel_group_dni.DoesNotExist:
            show_dni = False
        # print show_dni
        ctx = {
            "group": g, "template": template, "is_admin": _user_rel.is_admin, "is_secretary": _user_rel.is_secretary,
            "members": _members, "id_reunion": reunion, "secretary": _secretary, "president": _president, "show_dni": show_dni}
        return render_to_response('groups/rolesForMinutes.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/groups/' + str(g.slug) + "#necesitas-ser-redactor")


def getSignersList(m_signers):
    """
    this function is used for organize the signers in the minutes
    """
    list_ms = []
    list_temp = []
    i = 0
    for m in m_signers:
        try:
            _dni = DNI.objects.get(id_user=m.id_user)
            list_temp.append({"signer": m, "dni": _dni.dni_value, "dni_type": _dni.dni_type.short_name})
        except:
            list_temp.append({"signer": m, "dni": "", "dni_type": ""})
        if i >= 1:
            i = 0
            list_ms.append(list_temp)
            list_temp = []
        else:
            i = i + 1
    if i == 1:
        list_ms.append(list_temp)
    return (list_ms, list_temp)


@login_required(login_url='/account/login')
def newMinutes(request, slug_group, id_reunion, slug_template):
    '''
    This function creates a minutes with the form for this.
    '''
    saveViewsLog(request, "apps.groups_app.minutes.newMinutes")
    group = Groups.objects.get_group(slug=slug_group)

    _user_rel = getRelUserGroup(request.user, group.id)
    if _user_rel.is_secretary and _user_rel.is_active:
        saved = False
        error = False
        _reunion = None

        ######## <SLUG TEMPLATE> #########
        _template = getTemplateMinutes(slug_template)
        list_templates = getAllPublicTemplates()
        list_private_templates = getAllPrivateTemplates(id_group=group)
        ######## </SLUG TEMPLATE> #########

        ######## <MEMBER ASSISTANCE LISTS> #########
        members_assistant, members_no_assistant = getAssistanceFromRolUserMinutes(group)
        ######## </MEMBER ASSISTANCE LISTS> #########

        ######## <PRESIDENT AND SECRETARY> #########
        member_president, member_secretary = getPresidentAndSecretary(group)
        try:
            _dni_president = DNI.objects.get(id_user=member_president.id_user)
            president = {"user": member_president, "dni": _dni_president.dni_value, "dni_type": _dni_president.dni_type.short_name}
        except:
            president = {"user": member_president, "dni": "", "dni_type": ""}
        try:
            _dni_secretary = DNI.objects.get(id_user=member_secretary.id_user)
            secretary = {"user": member_secretary, "dni": _dni_secretary.dni_value, "dni_type": _dni_secretary.dni_type.short_name}
        except:
            secretary = {"user": member_secretary, "dni": "", "dni_type": ""}
        ######## </PRESIDENT AND SECRETARY> #########

        ######## <DNI> ########
        try:
            rgd = rel_group_dni.objects.get(id_group=group)
            show_dni = rgd.show_dni
        except:
            show_dni = False
        ######## </DNI> ########

        ######## <MEMBER SIGNERS LISTS> #########
        m_signers = getSignersFromRolUserMinutes(group)
        list_ms, list_temp = getSignersList(m_signers)
        ######## </MEMBER SIGNER LISTS> #########

        ######## <LOGO> #########
        url_logo = URL_BASE + '/static/img/logo_email.png'
        # if isProGroup(group):
        #     _pro = getProGroup(group)
        #     if _pro:
        #         url_logo = URL_BASE + _pro.id_organization.logo_address
        ######## </LOGO> #########

        ######## <SAVE_THE_MINUTE> #########
        if request.method == "POST":
            form = newMinutesForm(request.POST)
            # print "request.post------------------------------------"
            # print request.POST 
            # print "formulario--------------------------------"
            # print form 
            if form.is_valid():
                # print "form valid---------------------"
                _minute = saveMinute(request, group, form, _template)

                ######## <Create a relation into reunion and the new minutes> #########
                try:
                    id_reunion = int(request.POST.get('reunion_id'))
                except Exception:
                    id_reunion = None
                if id_reunion:
                    _reunion = getReunionById(id_reunion)

                if _minute and _reunion:
                        setRelationReunionMinutes(_reunion, _minute)
                ######## </Create a relation into reunion and the new minutes> #########

                if _minute:
                    ######## <asign DNI state> #######
                    rel_minutes_dni(id_minutes=_minute, show_dni=show_dni).save()
                    ######## <asign DNI state> #######

                    ######## <UPDATE_ROLES_IN_rol_user_minutes> #########
                    setMinuteAssistance(_minute, members_assistant, members_no_assistant)
                    url_new_minute = updateRolUserMinutes(request, group, _minute, for_approvers=True)
                    ######## </UPDATE_ROLES_IN_rol_user_minutes> #########
                    return HttpResponseRedirect(url_new_minute)
                else:
                    saved = False
                    error = "e2"  # error, mismo código de acta, o error al guardar en la db
            else:
                # print "form Invalid---------------------"
                saved = False
                error = "e0"  # error, el formulario no es valido
        ######## </SAVE_THE_MINUTE> #########

        ######## <SHOW_THE_MINUTE_FORM> #########
        else:
            form = newMinutesForm()
            _reunion = None
            if id_reunion:
                _reunion = getReunionById(id_reunion)
                if _reunion:
                    form = newMinutesForm(initial={"location": _reunion.locale})
        ######## <SHOW_THE_MINUTE_FORM> #########

        ######## <GET_LAST_MINUTES> #########
        last = getLastMinutes(group)
        ######## <GET_LAST_MINUTES> #########
        ctx = {'TITLE': "Nueva Acta",
               "newMinutesForm": form,
               "group": group,
               "rel_user": _user_rel,
               "reunion": _reunion,
               "minutes_saved": {"saved": saved, "error": error},
               "last": last,
               "members_selected": members_assistant,
               "members_no_selected":  members_no_assistant,
               "slug_template": slug_template,
               "minutesTemplateForm": _template.address_template,
               "minutesTemplateJs": _template.address_js,
               "list_templates": list_templates,
               "list_private_templates": list_private_templates,
               "members_signers": list_ms,
               "url_logo": url_logo,
               "president": president,
               "secretary": secretary,
               "show_dni": show_dni,
               "is_form": 1,
               "breadcrumb": _("Crear Acta")
               }
        return render_to_response('groups/templates/newMinutes.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/groups/" + group.slug + "#No-tienes-permiso-para-crear-actas")


def getExtraMinutesById(id_extra_minutes):
    try:
        return minutes_type_1.objects.get(id=id_extra_minutes)
    except minutes_type_1.DoesNotExist:
        return None


def setMinutesVersion(_minute, _extra_minutes, group, members_assistant,
    members_no_assistant, list_ms, president, secretary, show_dni, id_user_creator, url_logo):
    list_newMinutesForm = {
        "date_start": _extra_minutes.date_start,
        "date_end": _extra_minutes.date_end,
        "location": _extra_minutes.location,
        "agreement": _extra_minutes.agreement,
        "agenda": _extra_minutes.agenda,
        "type_reunion": _extra_minutes.type_reunion,
        "code": _minute.code}
    full_html = loader.render_to_string(_minute.id_template.address_template, {
        "URL_BASE": URL_BASE,
        "newMinutesForm": list_newMinutesForm,
        "group": group,
        "members_selected": members_assistant,
        "members_no_selected": members_no_assistant,
        "members_signers": list_ms,
        "url_logo": url_logo,
        "president": president,
        "secretary": secretary,
        "show_dni": show_dni,
        }
    )
    _minutes_version = minutes_version(id_minutes=_minute, id_user_creator=id_user_creator, full_html=full_html)
    _minutes_version.save()
    signs = getAllMinutesSigned(_minute)
    a = list()
    for s in signs:
        a.append(
            minutes_approver_version(
                id_user_approver=s.id_user,
                id_minutes_version=_minutes_version,
                is_signed_approved=s.is_signed_approved)
        )
    try:
        minutes_approver_version.objects.bulk_create(a)
    except Exception, e:
        print "Minutes.editMinute coping the approvers", e
    for s2 in signs:
        s2.is_signed_approved = 0
        s2.save()


@login_required(login_url='/account/login')
def editMinutes(request, slug_group, slug_template, minutes_code):
    '''This function creates a minutes with the form for this.'''
    saveViewsLog(request, "apps.groups_app.minutes.newMinutes")
    group = Groups.objects.get_group(slug=slug_group)

    _user_rel = getRelUserGroup(request.user, group.id)
    if _user_rel.is_secretary and _user_rel.is_active:
        saved = False
        error = False
        _reunion = None
        _minute = group.get_minutes_by_code(code=minutes_code)
        if _minute and not _minute.is_full_signed:
            _extra_minutes = getExtraMinutesById(_minute.id_extra_minutes)
            ######## <SLUG TEMPLATE> #########
            _template = getTemplateMinutes(slug_template)
            list_templates = getAllPublicTemplates()
            list_private_templates = getAllPrivateTemplates(id_group=group)
            ######## </SLUG TEMPLATE> #########

            ######## <MEMBER ASSISTANCE LISTS> #########
            members_assistant, members_no_assistant = getAssistanceFromRolUserMinutes(group, id_minutes=_minute)
            ######## </MEMBER ASSISTANCE LISTS> #########

            ######## <PRESIDENT AND SECRETARY> #########
            #member_president, member_secretary = getPresidentAndSecretary(group, minutes_current=_minute)
            ######## </PRESIDENT AND SECRETARY> #########

            ######## <PRESIDENT AND SECRETARY> #########
            member_president, member_secretary = getPresidentAndSecretary(group, minutes_current=_minute)
            try:
                _dni_president = DNI.objects.get(id_user=member_president.id_user)
                president = {"user": member_president, "dni": _dni_president.dni_value, "dni_type": _dni_president.dni_type.short_name}
            except:
                president = {"user": member_president, "dni": "", "dni_type": ""}
            try:
                _dni_secretary = DNI.objects.get(id_user=member_secretary.id_user)
                secretary = {"user": member_secretary, "dni": _dni_secretary.dni_value, "dni_type": _dni_secretary.dni_type.short_name}
            except:
                secretary = {"user": member_secretary, "dni": "", "dni_type": ""}
            ######## </PRESIDENT AND SECRETARY> #########

            ######## <DNI> ########
            try:
                rgd = rel_group_dni.objects.get(id_group=group)
                show_dni = rgd.show_dni
            except:
                show_dni = False
            ######## </DNI> ########

            ######## <MEMBER SIGNERS LISTS> #########
            m_signers = getSignersFromRolUserMinutes(group, id_minutes=_minute)
            list_ms, list_temp = getSignersList(m_signers)
            ######## </MEMBER SIGNER LISTS> #########

            ######## <LOGO> #########
            url_logo = URL_BASE + '/static/img/logo_email.png'
            # if isProGroup(group):
            #     _pro = getProGroup(group)
            #     if _pro:
            #         url_logo = URL_BASE + _pro.id_organization.logo_address
            ######## </LOGO> #########

            ######## <SAVE_THE_MINUTE> #########
            if request.method == "POST":
                form = newMinutesForm(request.POST)
                if form.is_valid():
                    is_other = None
                    # editar acta y poner un código ya existente, mirar la diferencia de formatos:
                    # print "------------------------", request.POST['date_start']
                    # print "------------------------", form.cleaned_data['date_start']
                    if form.cleaned_data['code'] != minutes_code:
                        # is_other = getMinutesByCode(group, form.cleaned_data['code'])
                        is_other = group.get_minutes_by_code(code=form.cleaned_data['code'])
                    if not is_other:
                        #guardad version
                        setMinutesVersion(_minute, _extra_minutes, group, members_assistant,
                            members_no_assistant, list_ms, president, secretary, show_dni, request.user, url_logo)
                        #/guardar versión
                        _minute = saveMinute(request, group, form, _template, id_minutes_update=_minute.pk)  # actualizar

                        if _minute:
                            ######## <UPDATE_ROLES_IN_rol_user_minutes> #########
                            # setMinuteAssistance(_minute, members_assistant, members_no_assistant)
                            url_new_minute = updateRolUserMinutes(request, group, _minute, for_approvers=True)
                            ######## </UPDATE_ROLES_IN_rol_user_minutes> #########

                            # send Email
                            return HttpResponseRedirect(url_new_minute)
                        else:
                            saved = False
                            error = "e2"  # error, mismo código de acta, o error al guardar en la db
                    else:
                        saved = False
                        error = "e2"  # error, mismo código de acta, o error al guardar en la db
                        # se redefinen las fechas ya que como vienen con otro formato (AM) no se imprimen de forma correcta en el form
                        request.POST['date_start'] = form.cleaned_data['date_start']
                        request.POST['date_end'] = form.cleaned_data['date_end']
                        form = newMinutesForm(request.POST)

                else:
                    saved = False
                    error = "e0"  # error, el formulario no es valido
            ######## </SAVE_THE_MINUTE> #########

            ######## <SHOW_THE_MINUTE_FORM> #########
            else:
                form = newMinutesForm()
                try:
                    if _extra_minutes:
                        date_1 = _extra_minutes.date_start
                        date_2 = _extra_minutes.date_end
                        form = newMinutesForm(
                            initial={
                            "code": _minute.code,
                            "date_start": date_1,
                            "date_end": date_2,
                            "location": _extra_minutes.location,
                            "agreement": _extra_minutes.agreement,
                            "agenda": _extra_minutes.agenda,
                            "type_reunion": _extra_minutes.type_reunion
                            }
                            )
                    _reunion = None
                except Exception, e:
                    print e
                    #saveActionLog "no se puede editar acta."
            ######## <SHOW_THE_MINUTE_FORM> #########

            ######## <GET_LAST_MINUTES> #########
            last = getLastMinutes(group)
            ######## <GET_LAST_MINUTES> #########
            ctx = {'title_edit': "Editar Acta",
                   "newMinutesForm": form,
                   "group": group,
                   "reunion": _reunion,
                   "minutes_saved": {"saved": saved, "error": error},
                   "last": last,
                   "members_selected": members_assistant,
                   "members_no_selected":  members_no_assistant,
                   "slug_template": slug_template,
                   "minutesTemplateForm": _template.address_template,
                   "minutesTemplateJs": _template.address_js,
                   "list_templates": list_templates,
                   "list_private_templates": list_private_templates,
                   "members_signers": list_ms,
                   "url_logo": url_logo,
                   "president": president,
                   "secretary": secretary,
                   "show_dni": show_dni,
                   "is_form": 1,
                   "is_edit": True,
                   "breadcrumb": _("Editar acta ")+minutes_code
                   }
            return render_to_response('groups/templates/newMinutes.html', ctx, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect("/groups/" + group.slug + "#No-existe-un-acta-con-codigo-" + minutes_code)
    else:
        return HttpResponseRedirect("/groups/" + group.slug + "#No-tienes-permiso-para-crear-actas")


@login_required(login_url='/account/login')
def saveMinute(request, group, form, _template, id_minutes_update=None):
    '''Save the minutes in the tables of data base: minutes_type_1, minutes
    return:'''
    saveViewsLog(request, "apps.groups_app.minutes.saveMinute")
    if getRelUserGroup(request.user, group).is_secretary:
        df = {
            'code': form.cleaned_data['code'],
            'date_start': form.cleaned_data['date_start'],
            'date_end': form.cleaned_data['date_end'],
            'location': form.cleaned_data['location'],
            'agenda': form.cleaned_data['agenda'],
            'agreement': form.cleaned_data['agreement'],
            'type_reunion': form.cleaned_data['type_reunion'],
        }
        if id_minutes_update:
            _minu = getMinutesById(id_minutes_update)
            _extra_minutes = getExtraMinutesById(_minu.id_extra_minutes)
            if _minu and _extra_minutes:
                _minu.code = df['code']
                _minu.is_full_signed = False
                _minu.id_template = _template
                _extra_minutes.date_start = df['date_start']
                _extra_minutes.date_end = df['date_end']
                _extra_minutes.location = df['location']
                _extra_minutes.agreement = df['agreement']
                _extra_minutes.agenda = df['agenda']
                _extra_minutes.type_reunion = df['type_reunion']

                _minu.save()
                _extra_minutes.save()
                return _minu  # the minute
            else:
                return False
        elif not getMinutesByCode(group, df['code']):
            myNewMinutes_type_1 = minutes_type_1(
                date_start=df['date_start'],
                date_end=df['date_end'],
                location=df['location'],
                agenda=df['agenda'],
                agreement=df['agreement'],
                type_reunion=df['type_reunion']
            )
            myNewMinutes_type_1.save()
            myNewMinutes = minutes(
                code=df['code'],
                id_extra_minutes=myNewMinutes_type_1.pk,
                id_group=group,
                id_template=_template,
                id_creator=request.user
            )
            myNewMinutes.save()
            id_user = request.user
            saveActionLog(id_user, 'NEW_MINUTE', "group: %s, code: %s" % (group.name, df['code']), request.META['REMOTE_ADDR'])
            # registra los usuarios que asistieron a la reunión en la que se creó el acta
            # setMinuteAssistance(myNewMinutes, m_selected, m_no_selected)
            return myNewMinutes
        else:
            return False
    else:
        return False


def getMinutesVersions(id_minutes):
    try:
        return minutes_version.objects.filter(id_minutes=id_minutes)
    except minutes_version.DoesNotExist:
        return None


@login_required(login_url='/account/login')
def showMinutes(request, slug, minutes_code):
    '''Muestra toda la informacion de un Acta (minutes) (DEPRECATED)'''
    # saveViewsLog(request, "apps.groups_app.minutes.showMinutes")
    group = getGroupBySlug(slug)
    if not group:
        return HttpResponseRedirect('/groups/#error-there-is-not-the-group')

    if isMemberOfGroup(request.user, group):
        minutes_current = getMinutesByCode(group, minutes_code)
        rel_group = getRelUserGroup(request.user, group)
        rol = getRolUserMinutes(request.user, group, id_minutes=minutes_current)

        rol_is_approver = False
        rel_group_is_secretary = False
        if rol:
            rol_is_approver = rol.is_approver
            rel_group_is_secretary = rel_group.is_secretary
        if rol_is_approver or rel_group_is_secretary or rel_group.is_secretary or rel_group.is_admin or minutes_current.is_full_signed:
            if not minutes_current:
                return HttpResponseRedirect('/groups/' + slug + '/#error-there-is-not-that-minutes')

            address_template = minutes_current.id_template.address_template
            address_js_template = minutes_current.id_template.address_js

            id_minutes_type = minutes_current.id_template.id_type.pk

            if id_minutes_type == 1:
                try:
                    data = minutes_type_1.objects.get(id=minutes_current.id_extra_minutes)
                except minutes_type_1.DoesNotExist:
                    data = None
                list_newMinutesForm = {
                    "date_start": data.date_start,
                    "date_end": data.date_end,
                    "location": data.location,
                    "agreement": data.agreement,
                    "agenda": data.agenda,
                    "type_reunion": data.type_reunion,
                    "code": minutes_current.code}

            if id_minutes_type == 2:  # para actas antiguas
                data = last_minutes.objects.get(id=minutes_current.id_extra_minutes)
                list_newMinutesForm = {
                    "address_file": MEDIA_URL + "lastMinutes/" + str(data.address_file).split("/")[len(str(data.address_file).split("/")) - 1],
                    "name_file": data.name_file}

            if id_minutes_type == 3:
                print "NO hay tres tipos de actas todavia"

            ######## <ASISTENTES> #########
            m_assistance, m_no_assistance = getMembersAssistance(group, minutes_current)
            ######## <ASISTENTES> #########

            ######## <DNI> ########
            try:
                rgd = rel_minutes_dni.objects.get(id_minutes=minutes_current)
                show_dni = rgd.show_dni
            except:
                show_dni = False
            ######## </DNI> ########

            ######## <SIGNERS> #########
            m_signers = getMembersSigners(group, minutes_current)
            list_ms = []
            list_temp = []
            i = 0
            for m in m_signers:
                try:
                    _dni = DNI.objects.get(id_user=m.id_user)
                    list_temp.append({"signer": m, "dni": _dni.dni_value, "dni_type": _dni.dni_type.short_name})
                except:
                    list_temp.append({"signer": m, "dni": "", "dni_type": ""})
                if i >= 1:
                    i = 0
                    list_ms.append(list_temp)
                    list_temp = []
                else:
                    i = i + 1
            if i == 1:
                list_ms.append(list_temp)
            ######## </SIGNERS> #########

            ######## <PRESIDENT AND SECRETARY> #########
            member_president, member_secretary = getPresidentAndSecretary(group, minutes_current)
            try:
                _dni_president = DNI.objects.get(id_user=member_president.id_user)
                president = {"user": member_president, "dni": _dni_president.dni_value, "dni_type": _dni_president.dni_type.short_name}
            except:
                president = {"user": member_president, "dni": "", "dni_type": ""}
            try:
                _dni_secretary = DNI.objects.get(id_user=member_secretary.id_user)
                secretary = {"user": member_secretary, "dni": _dni_secretary.dni_value, "dni_type": _dni_secretary.dni_type.short_name}
            except:
                secretary = {"user": member_secretary, "dni": "", "dni_type": ""}
            ######## </PRESIDENT AND SECRETARY> #########

            ######## <LOGO> #########
            url_logo = URL_BASE + '/static/img/logo_email.png'
            # if isProGroup(group):
            #     _pro = getProGroup(group)
            #     if _pro:
            #         url_logo = URL_BASE + _pro.id_organization.logo_address

            ######## </LOGO> #########

            ######## <ATTENDING> #########
            space_to_approve = False
            my_attending = False
            sign = getRelUserMinutesSigned(request.user, minutes_current)
            if sign:
                space_to_approve = True
                my_attending = True if sign.is_signed_approved == 0 else False
            ######## </ATTENDING> #########

            ######## <APPROVER LISTS> #########
            try:
                missing_approved_list = rel_user_minutes_signed.objects.filter(id_minutes=minutes_current)
                # missing_approved_list = 0 if len(missing_approved_list) == 0 else missing_approved_list
            except rel_user_minutes_signed.DoesNotExist:
                print "NO HAY rel_user_minutes_assistance missing_approved_list"
            except Exception, e:
                print "error,", e

            ######## </APPROVER LISTS> #########

            ######## <PREV and NEXT> #########
            prev, next = getPrevNextOfGroup(group, minutes_current)
            ######## </PREV and NEXT> #########

            annon = annotations.objects.filter(id_minutes=minutes_current).order_by("-date_joined")

            minutes_version = getMinutesVersions(minutes_current)

            ctx = {"is_org_admin": group.organization.has_user_role(request.user, "is_admin"),
                "group": group, "minutes": minutes_current, "prev": prev, "next": next, "is_secretary": rel_group.is_secretary,
                "m_assistance": m_assistance, "m_no_assistance": m_no_assistance, "pdf_address": pdf_address,
                "url_minute": request.get_full_path(),
                "minute_template": loader.render_to_string(address_template, {
                    "URL_BASE": URL_BASE,
                    "newMinutesForm": list_newMinutesForm,
                    "group": group,
                    "members_selected": m_assistance,
                    "members_no_selected": m_no_assistance,
                    "members_signers": list_ms,
                    "url_logo": url_logo,
                    "president": president,
                    "secretary": secretary,
                    "show_dni": show_dni
                    }),
                "space_to_approve": space_to_approve, "my_attending": my_attending,
                "commission_approving": missing_approved_list,
                "annotations": annon,
                "minutes_version": minutes_version,
                "minutesTemplateJs": address_js_template,
                "is_form": 0
            }
        else:
            return HttpResponseRedirect("/groups/" + slug + "#esta-acta-aun-no-ha-sido-aprobada")
        # else:
        #     return HttpResponseRedirect("/groups/" + slug + "#no-tienes-rol")
    else:
        return HttpResponseRedirect('/groups/#error-its-not-your-group')

    if request.method == 'GET':
        try:
            only_minutes = request.GET['only']
        except Exception, e:
            only_minutes = False
    if only_minutes:
        return render_to_response('groups/onlyShowMinutes.html', ctx, context_instance=RequestContext(request))
    else:
        return render_to_response('groups/showMinutes.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def uploadMinutes(request, slug_group):
    saveViewsLog(request, "apps.groups_app.minutes.uploadMinutes")
    group = Groups.objects.get(slug=slug_group, is_active=True)
    is_member = rel_user_group.objects.filter(id_group=group.id, id_user=request.user)
    datos_validos = ""
    if is_member:
        from apps.groups_app.forms import uploadMinutesForm
        if getRelUserGroup(request.user, group).is_secretary:
            if request.method == "POST":
                form = uploadMinutesForm(request.POST, request.FILES)
                if form.is_valid():
                    from apps.groups_app.validators import validateExtension
                    for f in request.FILES.getlist('minutesFile'):
                        if validateExtension(f.name):
                            _last_minutes = last_minutes(
                                id_user=request.user,
                                address_file=f,
                                name_file=f.name
                            )
                            import random
                            _last_minutes.save()
                            _minutes = minutes(
                                id_group=group,
                                id_creator=request.user,
                                id_extra_minutes=_last_minutes.pk,
                                id_template=templates.objects.get(pk=4),
                                is_valid=False,
                                is_full_signed=False,
                                code="%s-%s" % (int(random.random() * 1000000), _last_minutes.pk)
                            )
                            _minutes.save()
                        else:
                            print "invalid_extension in ", f.name
                else:
                    print "EL formulario no es valido"
            else:
                form = uploadMinutesForm()
                try:
                    datos_validos = request.GET['valid']
                except:
                    print ""
            last_minutes_list = []
            i = 0
            lml = minutes.objects.filter(id_group=group, id_template=templates.objects.get(pk=4), is_valid=False)
            for m in lml:
                last_minutes_list.append({'i': i, 'lm': last_minutes.objects.get(pk=m.id_extra_minutes).name_file, 'lm_id': last_minutes.objects.get(pk=m.id_extra_minutes).pk})
                i = i + 1
            _minutes = minutes.objects.filter(id_group=group, is_valid=True).order_by('-code')
            ctx = {
                'uploadMinutesForm': form,
                'group': group,
                'last_minutes': last_minutes_list,
                'datasize': len(last_minutes_list),
                'datos_validos': datos_validos,
                'minutes': _minutes}
            return render_to_response('groups/uploadMinutesForm.html', ctx, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect("/groups/" + group.slug + "?no_redactor=true")
    else:
        return HttpResponseRedirect('/groups/#error-view-group')


#@login_required(login_url='/account/login')
def uploadMinutesAjax(request):
    saveViewsLog(request, "apps.groups_app.minutes.uploadMinutesAjax")
    if request.is_ajax():
        if request.method == 'GET':
            try:
                last_minutes_get = request.GET['last_minutes']
            except Exception, e:
                last_minutes_get = False
            if last_minutes_get:
                a = json.loads(last_minutes_get)
                group_id = a['group_id']
                group = Groups.objects.get_or_none(pk=group_id)
                a = a['values']
                valid = True
                for m in a:
                    if not(a[m]['code'] == "") and not(getMinutesByCode(group, a[m]['code'])):
                        lm_temp = minutes.objects.get(id_extra_minutes=a[m]['lmid'], id_template=templates.objects.get(pk=4))
                        lm_temp.code = a[m]['code']
                        lm_temp.is_valid = True
                        lm_temp.save()
                    else:
                        valid = False
                if valid:
                    response = {'data': "validos"}
                else:
                    response = {'data': "no_validos"}
            else:
                response = {'data': "Error"}
        else:
            response = {'data': "No es GET"}
    else:
        response = {'data': "No es AJAX"}
    return HttpResponse(json.dumps(response), mimetype="application/json")


def deleteMinute(request):
    pass
