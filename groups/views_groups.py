#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.utils import simplejson as json

from django.contrib.auth.models import User
from groups.views import getGroupBySlug, getRelUserGroup
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
    pass