#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.utils import simplejson as json
from Actarium.settings import URL_BASE, MEDIA_URL

from django.contrib.auth.models import User
from groups.views import getGroupBySlug, getRelUserGroup, isMemberOfGroup, isProGroup, getProGroup
from groups.minutes import getMinutesByCode, getRolUserMinutes, getMembersAssistance, getMembersSigners, getPresidentAndSecretary, getRelUserMinutesSigned, getPrevNextOfGroup, getMinutesVersions
from groups.models import *
from actions_log.views import saveActionLog, saveViewsLog


def showHomeGroup(request, slug_group):
    '''
        Carga el menú de un grupo 
    '''
    g = getGroupBySlug(slug_group)
    ctx = {
        "group": g
    }
    return render_to_response("groups/templates/home.html", ctx, context_instance=RequestContext(request))


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
                "is_form": 0
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

