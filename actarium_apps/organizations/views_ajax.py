#encoding:utf-8
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required

from actarium_apps.organizations.models import Organizations, OrganizationsUser, OrganizationsRoles, rel_user_group
from apps.actions_log.views import saveActionLog, saveViewsLog
from apps.account.templatetags.gravatartag import showgravatar
from apps.groups_app.utils import getRelUserGroup
from apps.groups_app.validators import validateEmail
from apps.groups_app.utils import send_email_full_signed
import json


@login_required
def get_user_org_groups(request, slug_org=False):
    """Only org admin can use this function"""
    saveViewsLog(request, "actarium_apps.organizations.views_ajax.getListMembers")
    if not request.is_ajax():
        raise Http404
    if request.method == "GET":
        org = request.user.organizationsuser_user.get_org(slug=slug_org)
        uname = request.GET.get("uname")
        if uname:
            _user = User.objects.get_or_none(username=str(uname))
            if _user and org.has_user_role(_user, "is_member") or org.has_user_role(_user, "is_admin"):
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


@login_required
def getListMembers(request, slug_org=False):
    """Only org admin can use this function"""
    saveViewsLog(request, "actarium_apps.organizations.views_ajax.getListMembers")
    if not request.is_ajax():
        raise Http404
    if not (request.method == "GET"):
        raise Http404
    org = request.user.organizationsuser_user.get_org(slug=slug_org)
    if org and org.has_user_role(request.user, "is_admin"):
        search = request.GET.get('search')
        gid = request.GET.get('gid')
        if gid:
            group = org.get_group(id=gid)
        if validateEmail(search):
            try:
                ans = [User.objects.get(email=search)]
            except:
                ans = 1  # email valido, pero no es usuario
        else:
            ans1 = User.objects.filter(username__iregex=r"" + search + "")
            ans2 = User.objects.filter(email__iregex=r"" + search + "")
            ans3 = User.objects.filter(first_name__iregex=r"" + search + "")
            ans4 = User.objects.filter(last_name__iregex=r"" + search + "")
            ans = list(ans1) + list(ans2) + list(ans3) + list(ans4)
            
        if ans == 1:  # email valido, pero no es usuario
            user_info ={"user_id": search, "email": search, "username": search.split("@")[0].title(),
                    "gravatar": showgravatar(search, 30), "is_user": False}
            users = {"users": False, "new_user": user_info}
        else:
            users_json = []
            uids = []
            for u in ans:
                if u.id not in uids:
                    uids.append(u.id)
                    is_member = False
                    if gid:
                        rel = getRelUserGroup(u, group)
                        if rel:
                            is_member = True
                    users_json.append({
                        "id": u.id,
                        "username": u.username,
                        "full_name": u.get_full_name(),
                        "is_member": is_member,
                        "is_org_member": org.has_user_role(u, "is_member"),
                        "email": u.email,
                        "gravatar": showgravatar(u.email, 30)
                    })
            users = {"users": users_json, "new_user": False}
    else:
        users = {"forbbiden": _("No tienes permiso para agregar usuarios.")}
    return HttpResponse(json.dumps(users), mimetype="application/json")
    

@login_required
def config_admin_to_org(request, slug_org):
    """uname and set_admin come in POST method.
    set_admin is a number: 1=set admin, 0=remove admin"""
    if request.is_ajax():
        if request.method == "POST":
            org = request.user.organizationsuser_user.get_org(slug=slug_org)
            if org and org.has_user_role(request.user, "is_admin"):
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


@login_required
def delete_member_org(request, slug_org):
    """uname comes in POST method."""
    if request.is_ajax():
        if request.method == "POST":
            org = request.user.organizationsuser_user.get_org(slug=slug_org)
            if org and org.has_user_role(request.user, "is_admin"):
                uname = request.POST.get("uname")
                if uname:
                    _user = User.objects.get_or_none(username=str(uname))
                    if _user and org.has_user_role(_user, "is_member"):
                        #Eliminar de las comisiones aprobatorias
                        minutes_full_signed = org.delete_from_all_approvers_list(_user) # Retorna un listado de actas que se aprobaron al 
                        for m in minutes_full_signed: ## enviar correo notificando que se aprobo un acta
                            send_email_full_signed(m)
                        # eliminar grupos
                        org.delete_from_all_groups(_user)
                        # Eliminar de organizacion (Habilitar cupo)
                        org.delete_role(_user, is_member=True) ## el True se ignora, solo es para pasar como **kwarg
                        org.delete_role(_user, is_admin=True) ## el True se ignora, solo es para pasar como **kwarg

                        message = {"changed": True, "msj": "@" + _user.username + " " + _(u"ya no podrá acceder a la organización."), "num_members": org.get_num_members()}
                        saveActionLog(request.user, 'DEL_USER_ORG', "name: %s" % (org.name), request.META['REMOTE_ADDR'])
                    else:
                        message = {"error": _(u"Este usuario no pertenece a la organización")}
                else:
                    message = {"error": _(u"Faltan variables para realizar la operación, por favor recargue la página e intente de nuevo.")}
            else:
                message = {"forbbiden": _(u"No tienes permiso para eliminar miembros.")}
            return HttpResponse(json.dumps(message), mimetype="application/json")
    raise Http404


@login_required
def set_org_invitation(request, slug_org):
    if not request.is_ajax():
        raise Http404
    if not request.method == "POST":
        raise Http404
    org = request.user.organizationsuser_user.get_org(slug=slug_org)
    if org and org.has_user_role(request.user, "is_admin"):
        mail = request.POST.get("mail")
        uname = request.POST.get("uname")
        u = User.objects.get_or_none(email=mail, username=uname)
        message = {"error": _(u"No se agregó")}
        if u:
            if not org.has_user_role(u, "is_member"):
                org.set_role(u, is_member=True)
                user = {
                    "id": u.id,
                    "email": u.email,
                    "username": u.username,
                    "image": showgravatar(u.email, 28),
                    "full_name": u.get_full_name(),
                    "is_member": True
                }
                message = {"invited": _(u"%s ahora es miembro de la organización %s" % (u.get_full_name(), org.name)), "user": user}
            else:
                message = {"error": _(u"%s ya es miembro de la organización" % u.get_full_name())}
        return HttpResponse(json.dumps(message), mimetype="application/json")
