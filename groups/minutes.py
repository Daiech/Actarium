#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.http import Http404
from django.utils import simplejson as json

# imports from application
from groups.models import *
from groups.forms import newMinutesForm
from Actarium.settings import URL_BASE, MEDIA_URL
from account.templatetags.gravatartag import showgravatar

# Imports from views.py
from groups.views import getGroupBySlug, isMemberOfGroup, getRelUserGroup, get_user_or_email
from actions_log.views import saveActionLog
# from Actarium.settings import URL_BASE
from emailmodule.views import sendEmailHtml


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


def getMinutesById(minutes_id):  # not called
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
        return False
    except Exception, e:
        print "getRolUserMinutes Error", e
        return False


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


def getAssistanceFromRolUserMinutes(group):
    try:
        selected = rol_user_minutes.objects.filter(id_group=group, is_assistant=True, is_active=False)
        a = list()
        for m in selected:
            a.append(m.id_user.id)
        return getMembersOfGroupWithSelected(group, a)
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
        if role == 5:
            r = rol_user_minutes.objects.get(id_group=group, is_secretary=True, is_active=False)
            r.is_secretary = False
        r.save()
        return True
    except rol_user_minutes.DoesNotExist:
        return True
    except Exception:
        return False


def updateRolUserMinutes(request, group, _minute):
    try:
        rols = rol_user_minutes.objects.filter(id_group=group, is_active=False)

        email_list = list()
        for r in rols:
            if r.is_approver:
                email_list.append(r.id_user.email)
                print "SET:", setRelUserMinutesSigned(r.id_user, _minute, 0)

        rols.update(is_active=True, id_minutes=_minute)
    except Exception, e:
        print "newMinutes Error", e
        # saveErrorLog
    print "email_list", email_list
    url_new_minute = "/groups/" + str(group.slug) + "/minutes/" + str(_minute.code)
    link = URL_BASE + url_new_minute
    email_ctx = {
        'firstname': request.user.first_name,
        'username': request.user.username,
        'groupname': group.name,
        'link': link,
        'urlgravatar': showgravatar(request.user.email, 50)
    }
    sendEmailHtml(3, email_ctx, email_list)
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
    if request.is_ajax():
        if request.method == 'GET':
            try:
                minutes_id = str(request.GET['m_id'])
                approved = 1 if int(request.GET['approve']) == 1 else 2
                _minutes = getMinutesById(minutes_id)
                sign = getRelUserMinutesSigned(request.user, _minutes)
                if sign.is_signed_approved == 0:
                    sign.is_signed_approved = approved
                    sign.save()
            except Exception, e:
                print "Error Al Firmar" % e
            response = {"approved": approved, "minutes": minutes_id, "user-id": request.user.id, "user-name": request.user.first_name + " " + request.user.last_name}
    else:
        response = "Error invitacion"
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
                                rel.is_president = True
                            role_name = r4
                        if role == 5 and u and not remove:
                            if removeUniqueRolGroup(g, 5):
                                rel.is_secretary = True
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
            except groups.DoesNotExist:
                error = "Este grupo no existe"
            except rol_user_minutes.DoesNotExist:
                error = "Error! no existe el usuario para esta acta"
            except Exception, e:
                print "OCURRIO UN ERROR AL AGREGAR UN ROL:", e
                error = "Por favor recarga la p&aacute;gina e intenta de nuevo."
            if error:
                return HttpResponse(json.dumps({"error": error, "saved": False}), mimetype="application/json")
            response = {"saved": saved, "u": u.first_name, "role": role_name}
            return HttpResponse(json.dumps(response), mimetype="application/json")
    return HttpResponse(json.dumps({"error": "You can not enter here"}), mimetype="application/json")


@login_required(login_url='/account/login')
def rolesForMinutes(request, slug_group, id_reunion):
    '''
    return the board to give roles for a new minutes
    '''
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
        # members = rol_user_minutes.objects.filter(id_group=g, id_minutes=None, is_active=False)
        ctx = {"group": g, "is_admin": _user_rel.is_admin, "is_secretary": _user_rel.is_secretary, "members": _members, "id_reunion": reunion, "secretary": _secretary, "president": _president}
        return render_to_response('groups/rolesForMinutes.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/groups/' + str(g.slug) + "#necesitas-ser-redactor")


@login_required(login_url='/account/login')
def newMinutes(request, slug_group, id_reunion, slug_template):
    '''
    This function creates a minutes with the form for this.
    '''

    group = getGroupBySlug(slug_group)

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

        ######## <SAVE_THE_MINUTE> #########
        if request.method == "POST":
            form = newMinutesForm(request.POST)
            if form.is_valid():
                _minute = saveMinute(request, group, form, _template)

                ######## <Create a relation into reunion and the new minutes> #########
                try:
                    id_reunion = int(request.POST['reunion_id'])
                except Exception:
                    id_reunion = None
                if id_reunion:
                    _reunion = getReunionById(id_reunion)

                if _minute and _reunion:
                        setRelationReunionMinutes(_reunion, _minute)
                ######## </Create a relation into reunion and the new minutes> #########

                if _minute:
                    ######## <UPDATE_ROLES_IN_rol_user_minutes> #########
                    setMinuteAssistance(_minute, members_assistant, members_no_assistant)
                    url_new_minute = updateRolUserMinutes(request, group, _minute)
                    ######## </UPDATE_ROLES_IN_rol_user_minutes> #########
                    return HttpResponseRedirect(url_new_minute)
                else:
                    saved = False
                    error = "e2"  # error, mismo código de acta, o error al guardar en la db
            else:
                saved = False
                error = "e0"  # error, el formulario no es valido
        ######## </SAVE_THE_MINUTE> #########

        ######## <SHOW_THE_MINUTE_FORM> #########
        else:
            if id_reunion:
                _reunion = getReunionById(id_reunion)
                form = newMinutesForm(initial={"location": _reunion.locale})
            else:
                form = newMinutesForm()
                _reunion = None
        ######## <SHOW_THE_MINUTE_FORM> #########

        ######## <GET_LAST_MINUTES> #########
        last = getLastMinutes(group)
        ######## <GET_LAST_MINUTES> #########

        ctx = {'TITLE': "Nueva Acta",
               "newMinutesForm": form,
               "group": group,
               "reunion": _reunion,
               "minutes_saved": {"saved": saved, "error": error},
               "last": last,
               "members_selected": members_assistant,
               "members_no_selected":  members_no_assistant,
               "minutesTemplateForm": _template.address_template,
               "minutesTemplateJs": _template.address_js,
               "list_templates": list_templates,
               "list_private_templates": list_private_templates
               }
        return render_to_response('groups/newMinutes.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/groups/" + group.slug + "#No-tienes-permiso-para-crear-actas")


@login_required(login_url='/account/login')
def saveMinute(request, group, form, _template):
    '''
    Save the minutes in the tables of data base: minutes_type_1, minutes
    return:
    '''
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
        try:
            minu = minutes.objects.get(id_group=group, code=df['code'])
        except minutes.DoesNotExist:
            minu = None
        if not minu:
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


@login_required(login_url='/account/login')
def showMinutes(request, slug, minutes_code):
    '''
    Muestra toda la informacion de un Acta (minutes)
    '''
    pdf_address = 'false'
    if request.method == 'POST':
        html_data = request.POST['minutes-html-data']
        from pdfmodule.views import minutesHtmlToPdf
        pdf_address = minutesHtmlToPdf(html_data, slug)
        return HttpResponseRedirect(pdf_address)
    group = getGroupBySlug(slug)
    if not group:
        return HttpResponseRedirect('/groups/#error-there-is-not-the-group')

    if isMemberOfGroup(request.user, group):
        minutes_current = getMinutesByCode(group, minutes_code)
        rel_group = getRelUserGroup(request.user, group)
        rol = getRolUserMinutes(request.user, group, id_minutes=minutes_current)

        if rol:
            if rol.is_approver or rel_group.is_secretary:

                if not minutes_current:
                    return HttpResponseRedirect('/groups/' + slug + '/#error-there-is-not-that-minutes')

                address_template = minutes_current.id_template.address_template

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
                    missing_approved_list = rel_user_minutes_signed.objects.filter(id_minutes=minutes_current, is_signed_approved=0)
                    missing_approved_list = 0 if len(missing_approved_list) == 0 else missing_approved_list
                except rel_user_minutes_signed.DoesNotExist:
                    print "NO HAY rel_user_minutes_assistance missing_approved_list"
                except Exception, e:
                    print "error,", e

                approved_list = None
                no_approved_list = None
                try:
                    approved_list = rel_user_minutes_signed.objects.filter(id_minutes=minutes_current, is_signed_approved=1)
                    approved_list = 0 if len(approved_list) == 0 else approved_list
                except rel_user_minutes_signed.DoesNotExist:
                    print "NO HAY rel_user_minutes_assistance APPROVED_LIST"
                except Exception, e:
                    print "Error APPROVED_LIST,", e
                try:
                    no_approved_list = rel_user_minutes_signed.objects.filter(id_minutes=minutes_current, is_signed_approved=2)
                    no_approved_list = 0 if len(no_approved_list) == 0 else no_approved_list
                except rel_user_minutes_signed.DoesNotExist:
                    print "NO HAY rel_user_minutes_assistance NO_APPROVED_LIST"
                except Exception, e:
                    print "Error NO_APPROVED_LIST:", e

                ######## </APPROVER LISTS> #########

                ######## <PREV and NEXT> #########
                prev, next = getPrevNextOfGroup(group, minutes_current)
                ######## </PREV and NEXT> #########

                annon = annotations.objects.filter(id_user=request.user, id_minutes=minutes_current)

                ctx = {
                    "group": group, "minutes": minutes_current, "prev": prev, "next": next, "is_secretary": rel_group.is_secretary,
                    "m_assistance": m_assistance, "m_no_assistance": m_no_assistance, "pdf_address": pdf_address,
                    "minute_template": loader.render_to_string(address_template, {"newMinutesForm": list_newMinutesForm, "group": group, "members_selected": m_assistance, "members_no_selected": m_assistance}),
                    "space_to_approve": space_to_approve, "my_attending": my_attending,
                    "missing_approved_list": missing_approved_list,
                    "approved_list": approved_list, "no_approved_list": no_approved_list,
                    "annotations": annon
                }
            else:
                return HttpResponseRedirect("/groups/" + slug + "#esta-acta-aun-no-ha-sido-aprobada")
        else:
            return HttpResponseRedirect("/groups/" + slug + "#no-tienes-rol")
    else:
        return HttpResponseRedirect('/groups/#error-its-not-your-group')
    return render_to_response('groups/showMinutes.html', ctx, context_instance=RequestContext(request))



@login_required(login_url='/account/login')
def uploadMinutes(request, slug_group):
    group = groups.objects.get(slug=slug_group, is_active=True)
    is_member = rel_user_group.objects.filter(id_group=group.id, id_user=request.user)
    datos_validos = ""
    if is_member:
        from groups.forms import uploadMinutesForm
        if getRelUserGroup(request.user, group).is_secretary:
            if request.method == "POST":
                form = uploadMinutesForm(request.POST, request.FILES)
                if form.is_valid():
                    from groups.validators import validateExtension
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
                i = i+1
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
    if request.is_ajax():
        if request.method == 'GET':
            try:
                last_minutes_get = request.GET['last_minutes']
            except Exception, e:
                last_minutes_get = False
                print e
            if last_minutes_get:    
                print "last get", last_minutes_get
                a = json.loads(last_minutes_get)
                print "aaaaaaaaaaaa", a
                group_id = a['group_id']
                group = groups.objects.get(pk=group_id)
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
