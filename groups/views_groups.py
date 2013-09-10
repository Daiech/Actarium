#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader
from Actarium.settings import URL_BASE, MEDIA_URL

from django.contrib.auth.models import User
from groups.forms import newMinutesForm
from groups.views import getGroupBySlug, getRelUserGroup, isMemberOfGroup, isProGroup, getProGroup
from groups.minutes import getMinutesByCode, getRolUserMinutes, getMembersAssistance, getMembersSigners, getPresidentAndSecretary, getRelUserMinutesSigned, getPrevNextOfGroup, getMinutesVersions, getTemplateMinutes, getAllPublicTemplates, getAllPrivateTemplates, getAssistanceFromRolUserMinutes, getSignersFromRolUserMinutes, getSignersList, getLastMinutes
from groups.models import *
from actions_log.views import saveActionLog, saveViewsLog


@login_required(login_url='/account/login')
def showHomeGroup(request, slug_group):
    '''
        Carga el menú de un grupo 
    '''
    g = getGroupBySlug(slug_group)
    ctx = {
        "group": g
    }
    return render_to_response("groups/templates/home.html", ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def showTeamGroup(request, slug_group):
    saveViewsLog(request, "groups.views.groupSettings")
    try:
        u_selected = None
        if request.method == "GET":
            u = str(request.GET['u'])
            u_selected = User.objects.get(username=u).id
    except Exception:
        u_selected = None
    g = getGroupBySlug(slug_group)
    _user_rel = getRelUserGroup(request.user, g.id)
    if _user_rel.is_active:
        # if _user_rel.is_admin:
            members = rel_user_group.objects.filter(id_group=g.id).order_by("-is_active")
            ctx = {"group": g, "is_admin": _user_rel.is_admin, "is_member": _user_rel.is_member, "is_secretary": _user_rel.is_secretary, "members": members, "user_selected": u_selected}
            return render_to_response('groups/templates/team.html', ctx, context_instance=RequestContext(request))
        # else:
        #     return HttpResponseRedirect('/groups/' + str(g.slug) + "#redireccionado")
    else:
        return HttpResponseRedirect('/groups/' + str(g.slug) + "#redireccionado")
    # ctx = {
    #     "group": g
    # }
    return render_to_response("groups/templates/team.html", ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def showFolderGroup(request, slug_group):
    g = getGroupBySlug(slug_group)
    _user = getRelUserGroup(request.user, g)
    if _user:
        if _user.is_active:
            minutes_group = minutes.objects.filter(id_group=g.id, is_valid=True).order_by("-code")
            m = list()
            from groups.minutes import getRolUserMinutes
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
                "group": g, "current_member": _user, "minutes": m,
                'no_redactor': no_redactor}
            return render_to_response("groups/templates/folder.html", ctx, context_instance=RequestContext(request))
        return HttpResponseRedirect('/groups/#you-are-not-active')
    return HttpResponseRedirect('/groups/#error-view-group')


@login_required(login_url='/account/login')
def showCalendarGroup(request, slug_group):
    g = getGroupBySlug(slug_group)
    _user = getRelUserGroup(request.user, g)
    if _user:
        if _user.is_active:
            _reunions = reunions.objects.filter(id_group=g).order_by("date_reunion")
            ctx = {
                "group": g, "current_member": _user, "reunions": _reunions,
            }
            return render_to_response("groups/templates/calendar.html", ctx, context_instance=RequestContext(request))
        return HttpResponseRedirect('/groups/#you-are-not-active')
    return HttpResponseRedirect('/groups/#error-view-group')


@login_required(login_url='/account/login')
def showMinuteGroup(request, slug_group, minutes_code):
    '''
    Muestra toda la informacion de un Acta dentro de un grupo (minutes)
    '''
    saveViewsLog(request, "groups.minutes.showMinutes")
    pdf_address = 'false'
    if request.method == 'POST':
        html_data = request.POST['minutes-html-data']
        from pdfmodule.views import minutesHtmlToPdf
        pdf_address = minutesHtmlToPdf(html_data, slug_group)
        return HttpResponseRedirect(pdf_address)
    group = getGroupBySlug(slug_group)
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
            if isProGroup(group):
                _pro = getProGroup(group)
                if _pro:
                    url_logo = URL_BASE + _pro.id_organization.logo_address

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

            ctx = {
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
                "is_form": 0,
                "current_member": rel_group
            }
        else:
            return HttpResponseRedirect("/groups/" + slug_group + "#esta-acta-aun-no-ha-sido-aprobada")
        # else:
        #     return HttpResponseRedirect("/groups/" + slug_group + "#no-tienes-rol")
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
        return render_to_response('groups/templates/showMinutes.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def rolesForMinutes(request, slug_group, id_reunion):
    '''
    return the board to set the roles for a new Minutes
    '''
    saveViewsLog(request, "groups.minutes.rolesForMinutes")
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
        return render_to_response('groups/templates/rolesForMinutes.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/groups/' + str(g.slug) + "#necesitas-ser-redactor")


@login_required(login_url='/account/login')
def newMinutes(request, slug_group, id_reunion, slug_template):
    '''
    This function creates a minutes with the form for this.
    '''
    saveViewsLog(request, "groups.minutes.newMinutes")
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
        if isProGroup(group):
            _pro = getProGroup(group)
            if _pro:
                url_logo = URL_BASE + _pro.id_organization.logo_address
        ######## </LOGO> #########

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
               "is_form": 1
               }
        return render_to_response('groups/templates/newMinutes.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/groups/" + group.slug + "#No-tienes-permiso-para-crear-actas")
