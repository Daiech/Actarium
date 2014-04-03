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


@login_required(login_url='/account/login')
def change_role_member_org(request, slug_org):
    """uname and role come in POST method.
    role is a number: 1=admin, 2=member"""
    if request.is_ajax():
        if request.method == "POST":
            org = request.user.organizationsuser_user.get_org(slug=slug_org)
            if org.has_user_role(request.user, "is_admin"):
                uname = request.POST.get("uname")
                role = request.POST.get("role")
                if uname and role:
                    _user = User.objects.get_or_none(username=str(uname))
                    if _user and org.has_user_role(_user, "is_member") or org.has_user_role(_user, "is_admin"):
                        role = "is_admin" if role == "1" else "is_member"
                        rel = org.organizationsuser_organization.filter(user=_user, role__code=role, is_active=True)
                        if rel: # "YA TIENE ESTE ROL"
                            message = {"error": "@" + _user.username + " " + _(u"ya tiene éste rol.")}
                        else: # "PONGALE CON CONFIANZA"
                            _role = "is_admin" if role != "is_admin" else "is_member"
                            org.delete_role(_user, **{_role:True})
                            org.set_role(_user, **{role:True})
                            message = {"changed": True, "msj": _(u"El cambio de rol ha sido cambiado existosamente para") + " " + "@" + _user.username}
                else:
                    message = {"error": _(u"Ocurrió un error extraño, por favor recargue la página e intente de nuevo.")}
            else:
                message = {"forbbiden": _(u"No tienes permiso para agregar usuarios.")}
            return HttpResponse(json.dumps(message), mimetype="application/json")
    raise Http404