#encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

from actarium_apps.core.utils import create_default_service
from apps.actions_log.views import saveActionLog, saveViewsLog
from actarium_apps.organizations.models import Organizations, OrganizationsUser, OrganizationsRoles
from .forms import OrganizationForm
from .utils import saveOrganization


@login_required(login_url='/account/login')
def listOrgs(request):
    organizations = request.user.organizationsuser_user.get_orgs_by_role_code("is_member")
    return render(request, "organizations/read_orgs.html", locals())

#### ORGANIZATION CRUD #####
@login_required(login_url='/account/login')
def createOrg(request):
    saveViewsLog(request, "apps.groups_app.views_groups.createOrg")
    ref = request.GET.get('ref') if 'ref' in request.GET else ""
    if request.method == "POST":
        form = OrganizationForm(request.POST, request.FILES)
        if form.is_valid() and form.is_multipart():
            org = form.save()
            org.set_role(request.user, is_admin=True, is_member=True, is_creator=True)
            is_created, response = create_default_service(request.user, org)
            saveActionLog(request.user, 'NEW_ORG', "name: %s" % (org.name), request.META['REMOTE_ADDR'])
            return HttpResponseRedirect(org.get_absolute_url())
    else:
        form = OrganizationForm()
    return render(request, "organizations/create_org.html", locals())


@login_required(login_url='/account/login')
def readOrg(request, slug_org=False):
    if slug_org:
        org = request.user.organizationsuser_user.get_org(slug=slug_org)
        if org and org.has_user_role(request.user, "is_member"):
            return render(request, "organizations/index.html", locals())
        else:
            raise Http404
    return listOrgs(request)


@login_required(login_url='/account/login')
def deleteOrg(request, slug_org):
    org = request.user.organizationsuser_user.get_org(slug=slug_org)
    if org and org.has_user_role(request.user, "is_creator"):
        if request.method == "POST" and "archive" in request.POST:
            org.is_archived = True
            org.save()
            return HttpResponseRedirect(reverse("home") + "?org_archived=1")
        return render(request, "organizations/delete_org.html", locals())
    else:
        raise Http404
#### ORGANIZATION CRUD #####


@login_required(login_url='/account/login')
def settingsOrg(request, slug_org):
    org = request.user.organizationsuser_user.get_org(slug=slug_org)
    user_is_admin = org.has_user_role(request.user, "is_admin")
    if org and ('edit' in request.GET) and user_is_admin:
        update = True
        if request.method == "POST":
            form = OrganizationForm(request.POST, request.FILES, instance=org)
            if form.is_valid() and form.is_multipart():
                form.save()
                updated = saveActionLog(request.user, 'UPDATE_ORG', "name: %s" % (form.cleaned_data['name']), request.META['REMOTE_ADDR'])
                return HttpResponseRedirect(reverse("profile_org", args=(org.slug,)))
        else:
            form = OrganizationForm(instance=org)
    elif org and org.has_user_role(request.user, "is_member"):
        update = False
        current_members = org.get_num_members()
        max_members = org.organizationservices_organization.get_max_num_members()
        total = int(current_members)*100/int(max_members)
    else:
        raise Http404
    return render(request, "organizations/profile_org.html", locals())


@login_required(login_url='/account/login')
def teamOrg(request, slug_org):
    org = request.user.organizationsuser_user.get_org(slug=slug_org)
    if org:
        is_org_admin = org.has_user_role(request.user, "is_admin") # this var is needed in templates
        if is_org_admin or org.has_user_role(request.user, "is_member"):
            current_members = org.get_num_members()
            max_members = org.organizationservices_organization.get_max_num_members()
            total = int(current_members)*100/int(max_members)
            return render(request, "organizations/team_org.html", locals())
    raise Http404
