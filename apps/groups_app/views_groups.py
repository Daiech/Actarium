#encoding:utf-8
from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader
from django.http import Http404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from Actarium.settings import URL_BASE, MEDIA_URL
from django.contrib.auth.models import User
from apps.groups_app.forms import newMinutesForm, newGroupForm
from apps.groups_app.views import getRelUserGroup, isMemberOfGroup
from apps.groups_app.minutes import *
from apps.groups_app.models import *
from apps.emailmodule.models import *
from apps.actions_log.views import saveActionLog, saveViewsLog
from actarium_apps.organizations.models import rel_user_group
from .utils import create_group



@login_required(login_url='/account/login')
def showHomeGroup(request, slug_group):
    '''Carga el menú de un grupo'''
    g = Groups.objects.get_group(slug=slug_group)
    _user = getRelUserGroup(request.user, g)
    is_org_admin = g.organization.has_user_role(request.user, "is_admin")
    if is_org_admin or _user:
        if is_org_admin or _user.is_active:
            return HttpResponseRedirect(reverse("show_folder", args=(slug_group,)))
    raise Http404


@login_required(login_url='/account/login')
def showTeamGroup(request, slug_group):
    saveViewsLog(request, "apps.groups_app.views.showTeamGroup")
    try:
        u_selected = None
        if request.method == "GET":
            u = str(request.GET['u'])
            u_selected = User.objects.get(username=u).id
    except:
        u_selected = None
    g = Groups.objects.get_group(slug=slug_group)
    user_is_org_admin = g.organization.has_user_role(request.user, "is_admin")
    _user_rel = getRelUserGroup(request.user, g.id)
    if _user_rel or user_is_org_admin:
        if user_is_org_admin or _user_rel.is_active:
            members = rel_user_group.objects.filter(id_group=g.id).order_by("-is_active")
            is_m = _user_rel.is_member if( _user_rel and _user_rel.is_member) else user_is_org_admin
            is_s = _user_rel.is_secretary if (_user_rel and _user_rel.is_secretary) else user_is_org_admin
            ctx = {"user_is_org_admin": user_is_org_admin, "group": g, "rel_user": _user_rel, "is_member": is_m, "is_secretary": is_s, "members": members, "user_selected": u_selected, "breadcrumb":_("Equipo de trabajo")}
            return render(request, 'groups/templates/team.html', ctx)
        else:
            raise Http404
            return HttpResponseRedirect('/groups/' + str(g.slug) + "#not-active")
    else:
        raise Http404
    return render("groups/templates/team.html", ctx)


@login_required(login_url='/account/login')
def showFolderGroup(request, slug_group):
    saveViewsLog(request, "apps.groups_app.views.showFolderGroup")
    g = Groups.objects.get_group(slug=slug_group)
    _user = getRelUserGroup(request.user, g)
    is_org_admin = g.organization.has_user_role(request.user, "is_admin")
    if is_org_admin or _user:
        if is_org_admin or _user.is_active:
            minutes_group = minutes.objects.filter(id_group=g.id, is_valid=True).order_by("-date_created")
            m = list()
            for _minutes in minutes_group:
                m.append({
                    "minutes": _minutes,
                    "rol": getRolUserMinutes(request.user, g, id_minutes=_minutes)
                })
            if request.method == "GET":
                try:
                    # Say if the user can upload minutes
                    no_redactor = request.GET['no_redactor']
                except Exception:
                    no_redactor = 0
            ctx = {
                "group": g, "rel_user": _user, "minutes": m,
                'no_redactor': no_redactor,
                "breadcrumb":_("Folder de actas")}
            return render_to_response("groups/templates/folder.html", ctx, context_instance=RequestContext(request))
        return HttpResponseRedirect('/groups/#you-are-not-active')
    else:
        raise Http404


@login_required(login_url='/account/login')
def showCalendarGroup(request, slug_group):
    saveViewsLog(request, "apps.groups_app.views.showCalendarGroup")
    g = Groups.objects.get_group(slug=slug_group)
    _user = getRelUserGroup(request.user, g)
    is_org_admin = g.organization.has_user_role(request.user, "is_admin")
    if is_org_admin or _user:
        if is_org_admin or _user.is_active:
            _reunions = reunions.objects.filter(id_group=g).order_by("date_reunion")
            ctx = {"group": g, "rel_user": _user, "reunions": _reunions, "breadcrumb":_("Agenda de reuniones")}
            return render_to_response("groups/templates/calendar.html", ctx, context_instance=RequestContext(request))
        return HttpResponseRedirect('/groups/#you-are-not-active')
    return HttpResponseRedirect('/groups/#error-view-group')


@login_required(login_url='/account/login')
def showMinuteGroup(request, slug_group, minutes_code):
    '''Muestra toda la informacion de un Acta dentro de un grupo (minutes)'''
    saveViewsLog(request, "apps.groups_app.views.showMinuteGroup")
    group = Groups.objects.get_group(slug=slug_group)
    if not group:
        return HttpResponseRedirect('/groups/#error-there-is-not-the-group')
    is_org_admin = group.organization.has_user_role(request.user, "is_admin")
    if isMemberOfGroup(request.user, group) or is_org_admin:
        minutes_current = group.get_minutes_by_code(code=minutes_code)
        rel_group = getRelUserGroup(request.user, group)
        rol = getRolUserMinutes(request.user, group, id_minutes=minutes_current)

        rol_is_approver = False
        rel_group_is_secretary = False
        if rol and rel_group:
            rol_is_approver = rol.is_approver
            rel_group_is_secretary = rel_group.is_secretary
        if is_org_admin or (rel_group and rol_is_approver or rel_group_is_secretary or rel_group.is_secretary or rel_group.is_admin or minutes_current.is_minute_full_signed()):
            if not minutes_current:
                return HttpResponseRedirect('/groups/' + slug_group + '/#error-there-is-not-that-minutes')

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
                # missing_approved_list = rel_user_minutes_signed.objects.filter(id_minutes=minutes_current)
                missing_approved_list = group.rol_user_minutes_id_group.filter(id_minutes=minutes_current, is_active=True, is_approver=True)
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
            is_s = False
            if rel_group:
                is_s = rel_group.is_secretary
            ctx = {
                "group": group, "minutes": minutes_current, "prev": prev, "next": next,
                "rel_user": rel_group, "is_secretary": is_s,
                "m_assistance": m_assistance, "m_no_assistance": m_no_assistance,
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
                "is_form": 0,
                "breadcrumb":_("Acta ")+minutes_code
            }
        else:
            return HttpResponseRedirect("/groups/" + slug_group + "#esta-acta-aun-no-ha-sido-aprobada")
        # else:
        #     return HttpResponseRedirect("/groups/" + slug_group + "#no-tienes-rol")
    else:
        raise Http404
        # return HttpResponseRedirect('/groups/#error-its-not-your-group')

    if request.method == 'GET':
        try:
            only_minutes = request.GET['only']
        except Exception, e:
            only_minutes = False
    if only_minutes:
        return render_to_response('groups/onlyShowMinutes.html', ctx, context_instance=RequestContext(request))
    else:
        return render(request, 'minutes/show_minutes.html', ctx)


@login_required(login_url='/account/login')
def rolesForMinutes(request, slug_group, id_reunion):
    '''[DEPRECATED 07/07/14] return the board to set the roles for a new Minutes'''
    saveViewsLog(request, "apps.groups_app.minutes.rolesForMinutes")
    try:
        if id_reunion:
            reunion = reunions.objects.get(id=id_reunion).id
        else:
            reunion = ""
    except reunions.DoesNotExist:
        reunion = ""
    g = Groups.objects.get_group(slug=slug_group)
    _user_rel = getRelUserGroup(request.user, g.id)
    is_org_admin = g.organization.has_user_role(request.user, "is_admin")
    if is_org_admin or _user_rel.is_secretary and _user_rel.is_active:
        members = rel_user_group.objects.filter(id_group=g, is_member=True).order_by("-is_active")
        _members = list()
        for m in members:
            try:
                rel = rol_user_minutes.objects.get(id_group=g, id_user=m.id_user, id_minutes=None, is_active=False)
            except rol_user_minutes.DoesNotExist:
                rel = None
            except Exception, e:
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
            "group": g, "template": template, "rel_user": _user_rel,
            "members": _members, "id_reunion": reunion, "secretary": _secretary, "president": _president, "show_dni": show_dni,
            "breadcrumb":_("Definir roles")}
        return render_to_response('groups/templates/rolesForMinutes.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/groups/' + str(g.slug) + "#necesitas-ser-redactor")


@login_required(login_url='/account/login')
def configEmailNotifications(request, slug_group):
    from apps.groups_app.views import getGroupBySlug
    _group = getGroupBySlug(slug=slug_group)
    try:
        _user_rel = rel_user_group.objects.get(id_user=request.user, id_group=_group)
        _email_admin_type = email_admin_type.objects.get(name='grupo')
        _emails = email.objects.filter(admin_type=_email_admin_type)
        email_list = []
        for e in _emails:
            try:
                egp = email_group_permissions.objects.get(id_user=request.user, id_email_type=e.id, id_group=_group)
                checked = egp.is_active
            except email_group_permissions.DoesNotExist:
                checked = True
            except:
                return HttpResponseRedirect('/groups/#error-email-permissions')
            email_list.append({"id": e.id, "name": e.name, "description": e.description, "checked": checked})
        ctx = {"group": _group, "rel_user": _user_rel, "email_list": email_list,"breadcrumb":_("Config. notificaciones de correo")}
        return render_to_response('groups/templates/config_email.html', ctx, context_instance=RequestContext(request))
    except rel_user_group.DoesNotExist:
        return HttpResponseRedirect('/groups/#error-user-rel-group')


@login_required(login_url='/account/login')
def showGroupDNISettings(request, slug_group):
    '''
        Muestra la configuracion de DNI de los integrantes de un grupo
    '''
    saveViewsLog(request, "apps.groups_app.views.groupDNISettings")
    try:
        g = Groups.objects.get_group(slug=slug_group)
        _user_rel = getRelUserGroup(request.user, g)
        members_dni = DNI_permissions.objects.filter(id_group=g)
        users_dni = []
        for m in members_dni:
            users_dni.append(m.id_user)
        members = rel_user_group.objects.filter(id_group=g, is_member=True).exclude(id_user__in=users_dni)
        ctx = {"group": g, "rel_user": _user_rel, 'members': members, 'members_dni': members_dni,"breadcrumb":_("Config. DNI")}
        return render_to_response('groups/templates/showGroupDNI.html', ctx, context_instance=RequestContext(request))
    except groups.DoesNotExist:
        return HttpResponseRedirect('/groups/')


@login_required(login_url='/account/login')
def editInfoGroup(request, slug_group):
    '''
        Muestra la configuracion de un grupo
    '''
    saveViewsLog(request, "apps.groups_app.views.groupInfoSettings")
    g = Groups.objects.get_group(slug=slug_group)
    _user_rel = getRelUserGroup(request.user, g)
    if _user_rel.is_admin and _user_rel.is_active:
        message = False
        if request.method == "POST":
            form = newGroupForm(request.POST)
            if form.is_valid():
                g.name = form.cleaned_data['name']
                g.description = form.cleaned_data['description']
                g.save()
                message = "Los datos del grupo han sido actualizados"
            else:
                message = "Hubo un error en los datos del grupo. Intenta de nuevo."
        form = newGroupForm(initial={"name": g.name, "description": g.description})
        ctx = {"group": g, "rel_user": _user_rel, "form": form, "message": message,"breadcrumb":_(u"Editar información")}
        return render_to_response('groups/templates/editInfoGroup.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/groups/' + str(g.slug))





@login_required(login_url='/account/login')
def newGeneralGroup(request):
    saveViewsLog(request, "apps.groups_app.views_groups.newGeneralGroup")
    orgs = None
    sel_org = request.GET.get('org')
    if request.method == "POST":  # selecciona los datos para crear un nuevo grupo
        form = newGroupForm(request.POST)
        if form.is_valid():
            resp = create_group(request, form)
            if resp:
                saveActionLog(request.user, 'NEW_GROUP', "id_group: %s, group_name: %s, admin: %s" % (resp.pk, resp.name, request.user.username), request.META['REMOTE_ADDR'])
                return HttpResponseRedirect("/groups/" + str(resp.slug) + "?saved=1")
            else:
                pass ## No se pudo crear
    else:
        form = newGroupForm()
    orgs = request.user.organizationsuser_user.get_orgs_by_role_code("is_admin")
    ctx = {"newGroupForm": form,
           "organizations": orgs,
           "sel_org": sel_org,
           "full_path": request.get_full_path(),
           }
    return render(request, 'groups/templates/new_group.html', ctx)
