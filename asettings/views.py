#encoding:utf-8

from django.shortcuts import render_to_response
# from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
# from django.http import Http404
#from groups.models import groups, group_type, rel_user_group, minutes, invitations, minutes_type_1, minutes_type, reunions, admin_group, assistance, rel_user_minutes_assistance
#from groups.forms import newGroupForm, newMinutesForm, newReunionForm
#from django.contrib.auth.models import User
# from django.core.mail import EmailMessage
#import re
#import datetime
#from django.utils.timezone import make_aware, get_default_timezone, make_naive
#from django.utils import simplejson as json
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
def settings_billing(request):
    ctx = {'TITLE': "Actarium by Daiech"}
    return render_to_response('asettings/settings_billing.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/account/login')
def settings_organizations(request):
    ctx = {'TITLE': "Actarium by Daiech"}
    return render_to_response('asettings/settings_organization.html', ctx, context_instance=RequestContext(request))







