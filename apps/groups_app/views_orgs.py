#encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from apps.groups_app.forms import OrganizationForm
from apps.actions_log.views import saveActionLog, saveViewsLog
from .models import Organizations
from .utils import saveOrganization


@login_required(login_url='/account/login')
def createOrg(request):
    saveViewsLog(request, "apps.groups_app.views_groups.createOrg")
    ref = request.GET.get('ref') if 'ref' in request.GET else ""
    if request.method == "POST":
        form = OrganizationForm(request.POST, request.FILES)
        if form.is_valid() and form.is_multipart():
            ref = saveOrganization(request, form)
            saveActionLog(request.user, 'NEW_ORG', "name: %s" % (form.cleaned_data['name']), request.META['REMOTE_ADDR'])
            return HttpResponseRedirect(ref)
    else:
        form = OrganizationForm()
    return render(request, "groups_app/create_org.html", locals())


@login_required(login_url='/account/login')
def readOrg(request, slug_org=False):
    if slug_org:
        org = Organizations.objects.get_by_slug(slug_org)
        if org and request.user == org.admin:
            organizations = [org]
        else:
            raise Http404
    else:
        organizations = Organizations.objects.get_active_orgs(user=request.user)
    return render(request, "groups_app/read_orgs.html", locals())


@login_required(login_url='/account/login')
def updateOrg(request, slug_org):
    org = Organizations.objects.get_by_slug(slug_org)
    if org and request.user == org.admin:
        if request.method == "POST":
            form = OrganizationForm(request.POST, request.FILES, instance=org)
            if form.is_valid() and form.is_multipart():
                ref = saveOrganization(request, form)
                saveActionLog(request.user, 'UPDATE_ORG', "name: %s" % (form.cleaned_data['name']), request.META['REMOTE_ADDR'])
                return HttpResponseRedirect(ref)
        else:
            form = OrganizationForm(instance=org)
        return render(request, "groups_app/update_org.html", locals())
    else:
        raise Http404


@login_required(login_url='/account/login')
def deleteOrg(request, slug_org):
    org = Organizations.objects.get_by_slug(slug_org)
    if org and request.user == org.admin:
        if request.method == "POST" and "archive" in request.POST:
            pass
        return render(request, "groups_app/delete_org.html", locals())
    else:
        raise Http404
