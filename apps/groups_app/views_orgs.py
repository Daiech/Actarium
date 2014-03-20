#encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

from apps.groups_app.forms import OrganizationForm
from apps.actions_log.views import saveActionLog, saveViewsLog
from actarium_apps.organizations.models import Organizations, OrganizationsUser, OrganizationsRoles
from .utils import saveOrganization


@login_required(login_url='/account/login')
def createOrg(request):
    saveViewsLog(request, "apps.groups_app.views_groups.createOrg")
    ref = request.GET.get('ref') if 'ref' in request.GET else ""
    if request.method == "POST":
        form = OrganizationForm(request.POST, request.FILES)
        if form.is_valid() and form.is_multipart():
            org = form.save()
            org.set_role(request.user, is_admin=True, is_member=True, is_creator=True)
            from actarium_apps.core.utils import create_default_service
            is_created, response = create_default_service(request.user, org)
            print "::::::::::::::Respuesta",response
            saveActionLog(request.user, 'NEW_ORG', "name: %s" % (org.name), request.META['REMOTE_ADDR'])
            return HttpResponseRedirect(org.get_absolute_url())
    else:
        form = OrganizationForm()
    return render(request, "groups_app/create_org.html", locals())


@login_required(login_url='/account/login')
def readOrg(request, slug_org=False):
    if slug_org:
        org = request.user.organizationsuser_user.get_org(slug=slug_org)
        if org:
            organizations = [org]
        else:
            raise Http404
    else:
        organizations = request.user.organizationsuser_user.get_orgs_by_role_code("is_member")
    return render(request, "groups_app/read_orgs.html", locals())


@login_required(login_url='/account/login')
def updateOrg(request, slug_org):
    org = request.user.organizationsuser_user.get_org(slug=slug_org)
    if org and org.has_user_role(request.user, "is_admin"):
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
    org = request.user.organizationsuser_user.get_org(slug=slug_org)
    if org and org.has_user_role(request.user, "is_creator"):
        if request.method == "POST" and "archive" in request.POST:
            pass
        return render(request, "groups_app/delete_org.html", locals())
    else:
        raise Http404
