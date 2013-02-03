#encoding:utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
# from django.http import Http404
from groups.models import billing, packages
# group_type, rel_user_group, minutes, invitations, minutes_type_1, minutes_type, reunions, admin_group, assistance, rel_user_minutes_assistance
#from groups.forms import newGroupForm, newMinutesForm, newReunionForm
#from django.contrib.auth.models import User
# from django.core.mail import EmailMessage
#import re
import datetime
#from django.utils.timezone import make_aware, get_default_timezone, make_naive
from django.utils import simplejson as json
#from account.templatetags.gravatartag import showgravatar
#from django.core.mail import EmailMessage
#from actions_log.views import saveActionLog
#from Actarium.settings import URL_BASE

#def settings(request):
#    ctx = {'TITLE': "Actarium by Daiech"}
#    return render_to_response('website/settings_menu.html', ctx, context_instance=RequestContext(request))

#def settings_account(request):
#    ctx = {'TITLE': "Actarium by Daiech"}
#    return render_to_response('website/settings_account.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def settingsBilling(request):
    try:
        packages_list = packages.objects.filter(is_visible=True)
    except packages.DoesNotExist:
        packages_list = "No hay información disponible."
    try:
        billing_list = billing.objects.filter(is_active=True, id_user=request.user)
    except billing.DoesNotExist:
        billing_list = "No hay información disponible."
    ctx = {'TITLE': "Facturación - configuración", "packages_list": packages_list, "billing_list": billing_list}
    return render_to_response('asettings/settings_billing.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def settingsOrganizations(request):
    ctx = {'TITLE': "Actarium by Daiech"}
    return render_to_response('asettings/settings_organization.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def requestPackage(request):
    if request.is_ajax():
        if request.method == 'GET':
            id_pack = str(request.GET['id_package'])
            id_package = packages.objects.get(pk=id_pack)
            gpa = str(request.GET['gpa'])
            billing(id_package=id_package, id_user=request.user, groups_pro_available=gpa, date_start=datetime.date.today(), date_end=datetime.date.today()).save()
            is_billing_saved = "True"
        else:
            is_billing_saved = "False"
    else:
        is_billing_saved = "Error de servidor"
    return HttpResponse(json.dumps(is_billing_saved), mimetype="application/json")
