#encoding:utf-8
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required

from actarium_apps.organizations.models import Organizations, OrganizationsUser, OrganizationsRoles, rel_user_group
from apps.actions_log.views import saveActionLog, saveViewsLog
from apps.account.templatetags.gravatartag import showgravatar
from apps.groups_app.validators import validateEmail
import json


@login_required(login_url='/account/login')
def get_user_org_groups(request, slug_org=False):
    """Only org admin can use this function"""
    saveViewsLog(request, "actarium_apps.organizations.views_ajax.getListMembers")
    if request.is_ajax():
        if request.method == "GET":
            org = request.user.organizationsuser_user.get_org(slug=slug_org)
            uname = request.GET.get("uname")
            if uname:
                _user = User.objects.get_or_none(username=str(uname))
                if _user and org.has_user_role(_user, "is_member") or org.has_user_role(_user, "is_admin"):
                    print "USER", _user
                    my_group_list = []
                    for g in org.get_groups():
                        rel = rel_user_group.objects.get_rel(_user, g)
                        if rel:
                            my_group_list.append(
                                {"id": g.id,
                                "name": g.name,
                                "url": g.get_absolute_url(),
                                "image": g.image_path.url_100x100})
                    return HttpResponse(json.dumps(my_group_list), mimetype="application/json")
    raise Http404


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
    """uname and set_admin come in POST method.
    set_admin is a number: 1=set admin, 0=remove admin"""
    if request.is_ajax():
        if request.method == "POST":
            print request.POST
            org = request.user.organizationsuser_user.get_org(slug=slug_org)
            if org.has_user_role(request.user, "is_admin"):
                uname = request.POST.get("uname")
                set_admin = request.POST.get("set_admin")
                if uname and set_admin:
                    _user = User.objects.get_or_none(username=str(uname))
                    if _user and org.has_user_role(_user, "is_member"):
                        is_admin = org.organizationsuser_organization.get_or_none(user=_user, role__code="is_admin", is_active=True)
                        set_like_admin = True if set_admin == "1" else False
                        if not is_admin and set_like_admin: ## pongalo como admin
                            org.set_role(_user, is_admin=True)
                            message = {"changed": True, "msj": "@" + _user.username + " " + _(u"ahora es administrador de la organización.")}
                        elif is_admin and not set_like_admin: ## se quiere quitar admin
                            deleted = org.delete_role(_user, is_admin=True) ## el True se ignora, solo es para pasar como **kwarg
                            message = {"changed": True, "msj": "@" + _user.username + " " + _(u"ya no podrá administrar la organización.")}
                    else:
                        message = {"error": _(u"Este usuario no pertenece al grupo")}
                else:
                    message = {"error": _(u"Ocurrió un error extraño, por favor recargue la página e intente de nuevo.")}
            else:
                message = {"forbbiden": _(u"No tienes permiso para agregar usuarios.")}
            return HttpResponse(json.dumps(message), mimetype="application/json")
    raise Http404
