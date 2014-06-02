#encoding:utf-8
from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseRedirect
from django.template import RequestContext, loader
# from django.http import Http404
# from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

# from Actarium.settings import URL_BASE, MEDIA_URL
# from django.contrib.auth.models import User
# from apps.groups_app.forms import newMinutesForm, newGroupForm
# from apps.groups_app.views import getRelUserGroup, isMemberOfGroup
# from apps.groups_app.minutes import *
from apps.groups_app.models import *
# from apps.emailmodule.models import *
from apps.actions_log.views import saveActionLog, saveViewsLog
# from actarium_apps.organizations.models import rel_user_group
import datetime
from django.contrib.humanize.templatetags import humanize
from .utils_meetings import date_time_format_form, date_time_format_db, remove_gmt
import json


@login_required(login_url='/account/login')
def read_meetings(request, slug_group):
    from django.utils.timezone import make_aware, get_default_timezone, make_naive
    saveViewsLog(request, "apps.groups_app.views.calendar")
    # gr = Groups.objects.filter(rel_user_group__id_user=request.user)  # grupos
    gr = Groups.objects.get(slug=slug_group)
    # my_reu = reunions.objects.filter(id_group__in=gr, is_done=False).order_by("-date_convened")  # reuniones
    # my_reu_day = reunions.objects.filter(id_group__in=gr).order_by("-date_convened")  # reuniones para un dia
    my_reu = reunions.objects.filter(id_group=gr.id, is_done=False).order_by("-date_convened")  # reuniones
    my_reu_day = reunions.objects.filter(id_group=gr.id).order_by("-date_convened")  # reuniones para un dia
    i = 0
    json_array = {}
    for reunion in my_reu_day:
        td = make_naive(reunion.date_reunion, get_default_timezone()) - datetime.datetime.now()
        if not(td.days >= 0 and td.seconds >= 0 and td.microseconds >= 0):
            is_last = 1
        else:
            is_last = 0
        try:
            confirm = assistance.objects.get(id_user=request.user, id_reunion=reunion.pk)
            is_confirmed = confirm.is_confirmed
            is_saved = 1
        except assistance.DoesNotExist:
            is_confirmed = False
            is_saved = 0
        json_array[i] = {"id_r": str(reunion.id),
                         # "group":gr,
                         "group_slug": reunion.id_group.slug,
                         "group_name": reunion.id_group.name,
                         "date": humanize.naturaltime(reunion.date_reunion),
                         "date_normal": date_time_format_form(reunion.date_reunion),
                         'is_confirmed': str(is_confirmed),
                         'is_saved': is_saved,
                         "title": reunion.title,
                         'is_last': is_last}
        i = i + 1
    response = json_array
    ctx = {
        "reunions_day": my_reu,
        "reunions": my_reu,
        "my_reu_day_json": json.dumps(response),
        # "groups": gr,
        "group":gr,
        "breadcrumb":_("Mis reuniones"),
        }
    return render_to_response('groups/read_meetings.html', ctx, context_instance=RequestContext(request))



