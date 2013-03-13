#encoding:utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
# from django.http import Http404
from groups.models import billing, packages, organizations, groups_pro
# group_type, rel_user_group, minutes, invitations, minutes_type_1, minutes_type, reunions, admin_group, assistance, rel_user_minutes_assistance
from groups.forms import newOrganizationForm
#from django.contrib.auth.models import User
# from django.core.mail import EmailMessage
#import re
import datetime
# from dateutil.relativedelta import * 
#from django.utils.timezone import make_aware, get_default_timezone, make_naive
from django.utils import simplejson as json
#from account.templatetags.gravatartag import showgravatar
#from django.core.mail import EmailMessage
#from actions_log.views import saveActionLog
from Actarium.settings import MEDIA_ROOT, ORGS_IMG_DIR, MEDIA_URL

#def settings(request):
#    ctx = {'TITLE': "Actarium by Daiech"}
#    return render_to_response('website/settings_menu.html', ctx, context_instance=RequestContext(request))

#def settings_account(request):
#    ctx = {'TITLE': "Actarium by Daiech"}
#    return render_to_response('website/settings_account.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def settingsBilling(request):
    array_billing = []
    try:
        packages_list = packages.objects.filter(is_visible=True)
    except packages.DoesNotExist:
        packages_list = "No hay información disponible."
    try:
        billing_list = billing.objects.filter(id_user=request.user)
    except billing.DoesNotExist:
        billing_list = "No hay información disponible."
        for b in billing:
            array_billing[b.id] = int(p.time) * int(p.id_package.price)
    ctx = {'TITLE': "Facturación - configuración", "packages_list": packages_list, "billing_list": billing_list, 'array_billing': array_billing}
    return render_to_response('asettings/settings_billing.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def settingsOrganizations(request):
    if request.method == "GET":  # envia una variable para seleccionar una organizacion
        try:
            new_group = request.GET['saved']
        except Exception:
            new_group = False
    try:
        orgs = organizations.objects.filter(is_active=True, id_admin=request.user)
    except Exception, e:
        orgs = None
        raise e
    groups = list()
    for org in orgs:
        groups.append({"org": org, "groups_org_list": groups_pro.objects.filter(id_organization=org.id)})
    ctx = {"organizations": groups, "group_saved": new_group}
    return render_to_response('asettings/settings_organization.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def newOrganization(request):
    ref_get = ""
    if request.method == "GET":
        try:
            ref_get = request.GET['ref']
        except Exception:
            ref_get = "/settings/organizations"
    if request.method == "POST":
        form = newOrganizationForm(request.POST, request.FILES)
        if form.is_valid() and form.is_multipart():
            url = "/static/img/groups/default.jpg"
            org = organizations(
                id_admin=request.user,
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                logo_address=url)
            org.save()
            try:
                url_file = request.FILES['logo_address']
            except Exception:
                url_file = None
            if url_file:
                from django.template import defaultfilters
                url = save_file(url_file, defaultfilters.slugify(org.name) + "-" + str(org.id), path=ORGS_IMG_DIR)
                org.logo_address = url
                org.save()
            try:
                ref = request.POST['ref'] + "?org=" + str(org.id)
            except Exception:
                ref = ref_get
            return HttpResponseRedirect(ref)
    else:
        form = newOrganizationForm()
    ctx = {"form_org": form, "ref": ref_get}
    return render_to_response('asettings/settings_new_organization.html', ctx, context_instance=RequestContext(request))


def save_file(file, slug, path=''):
    ''' Little helper to save a file
    '''
    fd = open('%s/%s' % (MEDIA_ROOT, str(path) + str(slug)), 'wb')
    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()
    return MEDIA_URL + str(path) + str(slug)


@login_required(login_url='/account/login')
def requestPackage(request):
    if request.is_ajax():
        if request.method == 'GET':
            id_pack = str(request.GET['id_package'])
            id_package = packages.objects.get(pk=id_pack)
            gpa = str(request.GET['gpa'])
            time = str(request.GET['time'])
            billing(id_package=id_package, id_user=request.user, groups_pro_available=gpa, time=time).save()
            is_billing_saved = "True"
        else:
            is_billing_saved = "False"
    else:
        is_billing_saved = "Error de servidor"
    return HttpResponse(json.dumps(is_billing_saved), mimetype="application/json")


@login_required(login_url="/account/login")
def replyRequestPackage(request):
    if request.user.is_staff:
        ctx = {"billing_list": billing.objects.exclude(state=0).order_by("-date_request"),
                "billing_list2": billing.objects.filter(state='0').order_by("-date_request")
        }
        return render_to_response('asettings/settings_replyRequest.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


def setReplyRequestPackage(request):
    if request.is_ajax():
        if request.method == 'GET':
            id_billing = str(request.GET['id_billing'])
            state = str(request.GET['answer'])
            b = billing.objects.get(id=id_billing)
            mtim = b.time
            dtn = datetime.datetime.now()
            b.date_start = dtn
            dtn = dtn + datetime.timedelta(days=(30 * int(mtim)))
            b.date_end = dtn
            b.state = state
            b.save()
            is_billing_saved = "True"
        else:
            is_billing_saved = "False"
    else:
        is_billing_saved = "Error de servidor"
    return HttpResponse(json.dumps(is_billing_saved), mimetype="application/json")
