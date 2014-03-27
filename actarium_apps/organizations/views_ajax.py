#encoding:utf-8
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required

from actarium_apps.organizations.models import Organizations, OrganizationsUser, OrganizationsRoles
from apps.actions_log.views import saveActionLog, saveViewsLog
from apps.account.templatetags.gravatartag import showgravatar
from apps.groups_app.validators import validateEmail
import json


@login_required(login_url='/account/login')
def getListMembers(request, slug_org=False):
    """Only org admin can use this function"""
    saveViewsLog(request, "actarium_apps.organizations.views_ajax.getListMembers")
    if request.is_ajax():
        if request.method == "GET":
            org = request.user.organizationsuser_user.get_org(slug=slug_org)
            if org.has_user_role(request.user, "is_admin"):
                try:
                    search = request.GET.get('search')
                    valid_email = validateEmail(search)
                    if valid_email:
                        try:
                            ans = User.objects.get(email=search)
                        except User.DoesNotExist:
                            ans = 1  # email valido, pero no es usuario
                    else:
                        try:
                            ans = User.objects.get(username=search)
                        except User.DoesNotExist:
                            ans = 2  # no existe el usuario
                    if ans != 1 and ans != 2:
                        message = {
                            "user_id": ans.id,
                            "mail_is_valid": True,
                            "username": ans.username,
                            "is_user": True,
                            "mail": ans.email,
                            "gravatar": showgravatar(ans.email, 30)}
                    else:
                        if ans == 1:  # email valido, pero no es usuario
                            message = {"user_id": search, "mail_is_valid": True,
                                        "mail": search, "username": search.split("@")[0].title(),
                                        "gravatar": showgravatar(search, 30), "is_user": False}
                        else:
                            if ans == 2:  # no existe el usuario e email invalido
                                message = {"mail_is_valid": False}
                            else:
                                    message = False
                except Exception:
                    message = False
            else:
                message = {"forbbiden": _("No tienes permiso para agregar usuarios.")}
            return HttpResponse(json.dumps(message), mimetype="application/json")
        else:
            message = False
        return HttpResponse(message, mimetype="application/json")
    else:
        message = False
        return HttpResponse(message, mimetype="application/json")
