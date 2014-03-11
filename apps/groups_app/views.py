# Create your views here.
#encoding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import Http404
from apps.groups_app.models import *
from apps.groups_app.forms import newGroupForm, newReunionForm
from django.contrib.auth.models import User
import datetime
from django.utils.timezone import make_aware, get_default_timezone, make_naive
# from django.utils import simplejson as json
import json
from apps.account.templatetags.gravatartag import showgravatar
from apps.actions_log.views import saveActionLog, saveViewsLog
from Actarium.settings import URL_BASE
from apps.emailmodule.views import sendEmailHtml
from apps.groups_app.validators import validateEmail
from django.contrib.humanize.templatetags import humanize
from .utils import get_user_or_email, setUserRoles, getUserByEmail, getRelUserGroup, setRelUserGroup, sendInvitationToGroup, newUserWithInvitation


def isProGroup(group):
    try:
        groups_pro.objects.get(id_group=group, is_active=True)
        return True
    except groups_pro.DoesNotExist:
        return False


def getProGroup(group):
    try:
        return groups_pro.objects.get(id_group=group, is_active=True)
    except groups_pro.DoesNotExist:
        return False



def getUserById(id_user):
    try:
        _user = User.objects.get(id=id_user)
        return _user
    except User.DoesNotExist:
        return None


@login_required(login_url='/account/login')
def groupsList(request):
    '''
    lista los grupos del usuario registrado
    '''
    saveViewsLog(request, "apps.groups_app.views.groupList")
    try:
        #-----------------<INVITACIONES>-----------------
        my_inv = rel_user_group.objects.filter(id_user=request.user, is_active=False, is_member=True)
        #-----------------</INVITACIONES>-----------------
        mygroups = rel_user_group.objects.filter(id_user=request.user, is_active=True, is_member=True)
        my_admin_groups = rel_user_group.objects.filter(
            id_user=request.user,
            is_member=False,
            is_active=True,
            is_admin=True).order_by("date_joined")
    except rel_user_group.DoesNotExist:
        mygroups = "You Dont have any groups"
        my_admin_groups = "You Dont administrate any groups"

    ctx = {"groups": mygroups, "admin_groups": my_admin_groups, "invitations": my_inv}
    return render_to_response('groups/groupsList.html', ctx, context_instance=RequestContext(request))


def setRoltoUser(request, _user, _group, role, remove):
    '''
        rel is getRelUserGroup(u, g) where u is the user to set the rol
        role is an int to the role:
            Roles id:
            1 = member
            2 = writer
            3 = convener
            4 = admin
        remove is a boolean
    '''
    saveViewsLog(request, "apps.groups_app.views.setRoltoUser")
    rel = getRelUserGroup(_user, _group)
    if rel:
        role_name = False
        r = ["Miembro", "Redactor", "Convocador", "Administrador"]
        if not remove:
            if role == 1:
                rel.is_member = True
                role_name = r[0]
            if role == 2:
                rel.is_secretary = True
                role_name = r[1]
            if role == 3:
                rel.is_convener = True
                role_name = r[2]
            if role == 4:
                rel.is_admin = True
                role_name = r[3]
        if remove:
            if role == 1:
                rel.is_member = False
            if role == 2:
                rel.is_secretary = False
            if role == 3:
                rel.is_convener = False
            if role == 4 and not rel.is_superadmin:
                rel.is_admin = False
        rel.save()
        # saveAction added Rol: group: g, user: u, role = role, role name=role_name, set or remove?: remove
        if role_name:  # the rol has been assigned
            link = URL_BASE + "/groups/" + str(_group.slug)
            ctx_email = {
                'firstname': request.user.first_name,
                'username': request.user.username,
                'rolename': role_name,
                'groupname': _group.name,
                'grouplink': link,
                'urlgravatar': showgravatar(request.user.email, 50)
            }
            sendEmailHtml(4, ctx_email, [rel.id_user.email], _group)
        return True
    return False


def setRole(request, slug_group):
    """
        Set or remove role to a user
    """

    saveViewsLog(request, "apps.groups_app.views.setRole")
    error = False
    if request.is_ajax():
        if request.method == 'GET':
            try:
                g = groups.objects.get(slug=slug_group, is_active=True)
                _user_rel = getRelUserGroup(request.user, g)

                if _user_rel.is_admin:
                    role = int(request.GET['role'])
                    remove = bool(int(request.GET['remove']))
                    _user = get_user_or_email(request.GET['uid'])
                    u = _user['user']
                    if u:  # only if there are an user.
                        saved = setRoltoUser(request, u, g, role, remove)
                    else:
                        error = "El usuario no ha aceptado la invitaci&oacute;n"
                else:
                    error = "No tienes permiso para hacer eso, Por favor recarga la p&aacute;gina"
            except groups.DoesNotExist:
                error = "Este grupo no existe"
            except rel_user_group.DoesNotExist:
                error = "Error! no existe el usuario para este grupo"
            except Exception:
                error = "Por favor recarga la p&aacute;gina e intenta de nuevo."
            if error:
                return HttpResponse(json.dumps({"error": error, "saved": False}), mimetype="application/json")
            response = {"saved": saved, "u": u.first_name, "role": role}
            return HttpResponse(json.dumps(response), mimetype="application/json")
    return True


@login_required(login_url='/account/login')
def groupSettings(request, slug_group):
    '''
        Muestra la configuracion de un grupo para agregar usuarios y asignar roles
    '''
    saveViewsLog(request, "apps.groups_app.views.groupSettings")
    try:
        u_selected = None
        if request.method == "GET":
            u = str(request.GET['u'])
            u_selected = User.objects.get(username=u).id
    except Exception:
        u_selected = None
    g = getGroupBySlug(slug_group)
    _user_rel = getRelUserGroup(request.user, g.id)
    if _user_rel.is_active:
        if _user_rel.is_admin:
            members = rel_user_group.objects.filter(id_group=g.id).order_by("-is_active")
            ctx = {"group": g, "is_admin": _user_rel.is_admin, "is_member": _user_rel.is_member, "is_secretary": _user_rel.is_secretary, "members": members, "user_selected": u_selected}
            return render_to_response('groups/adminRolesGroup.html', ctx, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('/groups/' + str(g.slug))
    else:
        return HttpResponseRedirect('/groups/' + str(g.slug))


@login_required(login_url='/account/login')
def groupInfoSettings(request, slug_group):
    '''
        Muestra la configuracion de un grupo
    '''
    saveViewsLog(request, "apps.groups_app.views.groupInfoSettings")
    try:
        g = groups.objects.get(slug=slug_group, is_active=True)
    except groups.DoesNotExist:
        raise Http404
    _user_rel = getRelUserGroup(request.user, g)
    if _user_rel.is_admin and _user_rel.is_active:
        message = False
        if request.method == "POST":
            form = newGroupForm(request.POST)
            if form.is_valid():
                g.name = form.cleaned_data['name']
                g.description = form.cleaned_data['description']
                g.save()
                message = "Los datos del grupo han sido actualizados"
            else:
                message = "Hubo un error en los datos del grupo. Intenta de nuevo."
        form = newGroupForm(initial={"name": g.name, "description": g.description})
        ctx = {"group": g, "is_admin": _user_rel.is_admin, "form": form, "message": message}
        return render_to_response('groups/adminInfoGroup.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/groups/' + str(g.slug))


@login_required(login_url='/account/login')
def groupDNISettings(request, slug_group):
    '''
        Muestra la configuracion de DNI de los integrantes de un grupo
    '''
    #    gr = groups.objects.filter(rel_user_group__id_user=request.user)  # grupos
    #    my_reu = reunions.objects.filter(id_group__in=gr, is_done=False).order_by("-date_convened")  # reuniones
    #    dateslug_min = str(make_aware(datetime.datetime.strptime(slug + " 00:00:00", '%Y-%m-%d %H:%M:%S'), get_default_timezone()))
    #    dateslug_max = str(make_aware(datetime.datetime.strptime(slug + " 23:59:59", '%Y-%m-%d %H:%M:%S'), get_default_timezone()))
    #    my_reu_day = reunions.objects.filter(id_group__in=gr, date_reunion__range=[dateslug_min, dateslug_max]).order_by("-date_convened")  # reuniones para un dia
    saveViewsLog(request, "apps.groups_app.views.groupDNISettings")
    try:
        g = groups.objects.get(slug=slug_group, is_active=True)
        _user_rel = getRelUserGroup(request.user, g)
        members_dni = DNI_permissions.objects.filter(id_group=g)
        users_dni = []
        for m in members_dni:
            users_dni.append(m.id_user)
        members = rel_user_group.objects.filter(id_group=g, is_member=True).exclude(id_user__in=users_dni)
        ctx = {"group": g, "is_admin": _user_rel.is_admin, 'members': members, 'members_dni': members_dni}
        return render_to_response('groups/adminDNIGroup.html', ctx, context_instance=RequestContext(request))
    except groups.DoesNotExist:
        return HttpResponseRedirect('/groups/')


def requestDNI(request, slug_group):
    """
        Sen request for DNI
    """
    saveViewsLog(request, "apps.groups_app.views.requestDNI")
    error = False
    saved = False
    if request.is_ajax():
        if request.method == 'GET':
            try:
                g = groups.objects.get(slug=slug_group, is_active=True)
                _user_rel = getRelUserGroup(request.user, g)

                if _user_rel.is_admin:
                    try:
                        id_user = User.objects.get(pk=int(request.GET['pk_user']))
                        DNI_per = DNI_permissions(id_group=g, id_user=id_user, id_requester=request.user)
                        DNI_per.save()
                        saved = True
                        email = [id_user.email]
                        ctx_email = {
                            'firstname': request.user.first_name + request.user.last_name,
                            'username': request.user.username,
                            'groupname': g.name,
                            'urlgravatar': showgravatar(request.user.email, 50)
                        }
                        sendEmailHtml(14, ctx_email, email)
                    except:
                        saved = False
                        error = "Ha ocurrido un error inesperado al enviar la solicitud, por favor intentalo de nuevo mas tarde"
                else:
                    error = "No tienes permiso para hacer eso, Por favor recarga la p&aacute;gina"
            except groups.DoesNotExist:
                error = "Este grupo no existe"
            except rel_user_group.DoesNotExist:
                error = "Error! no existe el usuario para este grupo"
            except Exception:
                error = "Por favor recarga la p&aacute;gina e intenta de nuevo."
            if error:
                return HttpResponse(json.dumps({"error": error, "saved": False}), mimetype="application/json")
            response = {"saved": saved, "error": error}
            return HttpResponse(json.dumps(response), mimetype="application/json")
        else:
            return "Ha ocurrido un error"
    return True


@login_required(login_url='/account/login')
def newBasicGroup(request, form, pro=False):
    saveViewsLog(request, "apps.groups_app.views.newBasicGroup")
    df = {
        'name': form.cleaned_data['name'],
        'description': form.cleaned_data['description'],
        'id_creator': request.user,
        # 'id_group_type': form.cleaned_data['id_group_type']  # Se omite para no pedir tipo de grupo
        'id_group_type': 1
    }
    myNewGroup = groups(
        name=df['name'],
        description=df['description'],
        id_creator=df['id_creator'],
        id_group_type=group_type.objects.get(pk=df['id_group_type']),
    )
    myNewGroup.save()
    if not pro:  # new rel to: Create free group
        setRelUserGroup(id_user=request.user, id_group=myNewGroup, is_superadmin=1, is_admin=1, is_active=True)
    else:
        try:
            user_or_email = get_user_or_email(request.POST.get('id_admin'))
        except Exception:
            user_or_email = {"user": None}
        if user_or_email:  # <-- the admin
            try:
                is_memb = int(request.POST['is_member'])
            except Exception:
                is_memb = 0
            if is_memb:  # new rel to: Create group. I'm member
                setUserRoles(request.user, myNewGroup, is_member=1, is_active=True)
            if user_or_email['user'] != request.user:
                if user_or_email['user']:
                    inv = sendInvitationToGroup(user_or_email['user'], request.user, myNewGroup)
                    if inv:  # new rel to: Create group. Other is admin (other) # this is the group than only i administer
                        setUserRoles(user_or_email['user'], myNewGroup, is_superadmin=1, is_admin=1, is_active=False)
                else:
                    _user = newUserWithInvitation(user_or_email['email'], request.user, myNewGroup)
                    if _user:  # new rel to: Create group. Other is admin (other)
                        setUserRoles(_user, myNewGroup, is_superadmin=1, is_admin=1, is_active=False)

            else:  # new rel to: Create group. I'm admin
                setUserRoles(user_or_email['user'], myNewGroup, is_superadmin=1, is_admin=1, is_member=is_memb, is_active=1)
                print getRelUserGroup(user_or_email['user'], myNewGroup).is_admin
        else:
            print "No hay un administrador para este grupo"  # error! se dio atras al crear new group y no se selecciono un admin
    return myNewGroup


@login_required(login_url='/account/login')
def newProGroup(request, form):
    saveViewsLog(request, "apps.groups_app.views.newProGroup")
    # print "type-group: %s , id-organization: %s, id-billing: %s" % (request.POST['type-group'], request.POST['sel-organization'], request.POST['sel-billing'])
    org_id = request.POST.get('sel-organization')
    try:
        org = organizations.objects.get(id=ord_id, id_admin=request.user, is_active=True)
    except organizations.DoesNotExist:
        org = None
    except Exception:
        org = False
    try:
        bill = billing.objects.get(id=request.POST['sel-billing'], id_user=request.user, state='1')
    except billing.DoesNotExist:
        bill = None
    except Exception:
        bill = False
    if org and bill:
        if bill.groups_pro_available >= 1:
            new_group = newBasicGroup(request, form, pro=True)
            g_pro = groups_pro(id_group=new_group, id_organization=org, id_billing=bill)
            g_pro.save()
            bill.groups_pro_available = bill.groups_pro_available - 1
            bill.save()
            return new_group
        else:
            return False
    else:
        return False


@login_required(login_url='/account/login')
def getProGroupDataForm(request):
    saveViewsLog(request, "apps.groups_app.views.getProGroupDataForm")
    orgs = None
    billing_list = None
    try:
        orgs = organizations.objects.filter(is_active=True, id_admin=request.user)
    except Exception, e:
        orgs = None
        raise e
    try:
        billing_list = billing.objects.filter(state='1', id_user=request.user, groups_pro_available__gte=1)
    except billing.DoesNotExist:
        billing_list = u"No hay información disponible."
    return (orgs, billing_list)


@login_required(login_url='/account/login')
def newGroup(request):
    '''
        crea una nuevo grupo
    '''
    saveViewsLog(request, "apps.groups_app.views.newGroup")
    orgs = None
    billing_list = None
    no_billing_avalaible = False  # indica si se intento crear un grupo pro sin paquetes disponibles
    sel_org = False
    if request.method == "GET":  # envia una variable para seleccionar una organizacion
        try:
            sel_org = request.GET['org']
        except Exception:
            sel_org = False

    if request.method == "POST":  # selecciona los datos para crear un nuevo grupo
        form = newGroupForm(request.POST)
        if form.is_valid():
            if int(request.POST['type-group']) == 0:  # 0 = grupo Free
                resp = newBasicGroup(request, form)
            else:
                resp = newProGroup(request, form)
                if resp:
                    resp.is_pro = True
                    resp.save()
            if resp:
                saveActionLog(request.user, 'NEW_GROUP', "id_group: %s, group_name: %s, admin: %s" % (resp.pk, resp.name, request.user.username), request.META['REMOTE_ADDR'])
                return HttpResponseRedirect("/groups/" + str(resp.slug) + "?saved=1")
            else:
                no_billing_avalaible = True
    else:
        form = newGroupForm()
    orgs, billing_list = getProGroupDataForm(request)
    ctx = {"newGroupForm": form,
           "organizations": orgs,
           "billing": billing_list,
           "sel_org": sel_org,
           "full_path": request.get_full_path(),
           "no_billing_avalaible": no_billing_avalaible
           }
    return render_to_response('groups/newGroup.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def showGroup(request, slug):
    '''
        Muestra la informacion de un grupo
    '''
    saveViewsLog(request, "apps.groups_app.views.showGroup")
    try:
        g = groups.objects.get(slug=slug, is_active=True)
        _user = getRelUserGroup(request.user, g)
        if _user:
            if _user.is_active:
                members = rel_user_group.objects.filter(id_group=g.id, is_member=True).order_by("-is_active")
                _reunions = reunions.objects.filter(id_group=g).order_by("date_reunion")
                minutes_group = minutes.objects.filter(id_group=g.id, is_valid=True).order_by("-code")
                m = list()
                from apps.groups_app.minutes import getRolUserMinutes
                for _minutes in minutes_group:
                    m.append({
                        "minutes": _minutes,
                        "rol": getRolUserMinutes(request.user, g, id_minutes=_minutes)
                    })
                if request.method == "GET":
                    try:
                        # Say if the user can upload minutes
                        no_redactor = request.GET['no_redactor']
                    except Exception:
                        no_redactor = 0
                pro = False
                if isProGroup(g):
                    pro = getProGroup(g)
                ctx = {
                    "group": g, "current_member": _user, "members": members, "minutes": m, "reunions": _reunions,
                    "now_": datetime.datetime.now(), 'no_redactor': no_redactor, "is_pro": pro}
                return render_to_response('groups/showGroup.html', ctx, context_instance=RequestContext(request))

            if _user.is_admin and _user.is_active:
                return HttpResponseRedirect('/groups/' + str(g.slug) + "/admin")

            if _user.is_superadmin and _user.is_active:
                return HttpResponseRedirect("/settings/organizations")

            if not _user.is_active:
                return HttpResponseRedirect('/groups/' + "?group=" + str(g.slug))
        # request.user is the org admin of this group? redirect to /settings/organizations

        if isProGroup(g):
            pro = getProGroup(g)
            if pro.id_organization.id_admin == request.user:
                saved = 0
                if request.method == "GET":
                    try:
                        saved = request.GET['saved']
                    except Exception:
                        saved = 0
                    return HttpResponseRedirect("/settings/organizations?saved=" + str(saved))
        return HttpResponseRedirect('/groups/#error-view-group')
    except groups.DoesNotExist:
        raise Http404
    except rel_user_group.DoesNotExist:
        raise Http404


@login_required(login_url='/account/login')
def getMembers(request):
    saveViewsLog(request, "apps.groups_app.views.getMembers")
    if request.is_ajax():
        if request.method == "GET":
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
            return HttpResponse(json.dumps(message), mimetype="application/json")
        else:
            message = False
        return HttpResponse(message)
    else:
        message = False
        return HttpResponse(message)


def isMemberOfGroup(id_user, id_group):
    try:
        _member = getRelUserGroup(id_user, id_group)
        if _member:
            return True
        else:
            return False
    except rel_user_group.DoesNotExist:
        print "No hay este usuario en este grupo"
        return False
    except Exception, e:
        print "El usuario no existe, Exception: %s" % e
        return False


def isMemberOfGroupByEmail(email, id_group):
    if validateEmail(str(email)):
        try:
            ans = getUserByEmail(email)
            if ans:
                return isMemberOfGroup(ans, id_group)
            else:
                return False
        except User.DoesNotExist:
            return False
        except Exception:
            return False
    else:
        return False


#@requires_csrf_token  # pilas con esto, es para poder enviar los datos via POST
@login_required(login_url='/account/login')
def newInvitationToGroup(request):
    saveViewsLog(request, "apps.groups_app.views.newInvitationToGroup")
    if request.is_ajax():
        if request.method == 'GET':
            _user_rel = False
            try:
                g = groups.objects.get(pk=request.GET['pk'])
                _user_rel = getRelUserGroup(request.user, g)
                if not (_user_rel.is_admin or _user_rel.is_secretary):
                    return HttpResponse(json.dumps({"error": "permiso denegado"}), mimetype="application/json")
            except groups.DoesNotExist:
                g = False
                return HttpResponse(json.dumps({"error": "Ocurri&oacute; un error, estamos trabajando para resolverlo. Si el error persiste, comun&iacute;cate con el administrador de Actarium en <a href='mailto:soporte@daiech.com'>soporte@daiech.com</a>"}), mimetype="application/json")
            except Exception, e:
                print "Exception newInvitationToGroup: " % e
                g = False
                return HttpResponse(json.dumps({"error": "Ocurri&oacute; un error, estamos trabajando para resolverlo."}), mimetype="application/json")
            if _user_rel.is_admin:
                email = str(request.GET['mail'])
                firstname = None
                lastname = None
                try:
                    if request.GET['new'] == "1":
                        firstname = str(request.GET['firstname'])
                        lastname = str(request.GET['lastname'])
                except Exception:
                    firstname = None
                    lastname = None
                if isMemberOfGroupByEmail(email, g):
                    invited = False
                    message = "El usuario ya es miembro del grupo"
                    iid = False
                    gravatar = False
                else:
                    _user = getUserByEmail(email)
                    if not _user:
                        _user = newUserWithInvitation(email, request.user, g, first_name=firstname, last_name=lastname)
                    sendInvitationToGroup(_user, request.user, g)
                    if _user and not (_user is 0):  # 0 = is email failed
                        try:
                            invited = True
                            iid = str(_user.id)  # get de id from invitation
                            gravatar = showgravatar(email, 30)
                            message = u"Se ha enviado la invitación a " + str(email) + " al grupo <strong>" + g.name + "</strong>"
                            saveActionLog(request.user, 'SEN_INVITA', "email: %s" % (email), request.META['REMOTE_ADDR'])  # Accion de aceptar invitacion a grupo
                        except Exception, e:
                            print e
                    else:
                        iid = False
                        invited = False
                        gravatar = False
                        if not _user and not (_user is 0):
                            message = "El email que estas tratando de registrar ya tiene una cuenta."
                            # message = u"El usuario tiene la invitación pendiente"
                        else:
                            if _user == 0:
                                message = "El correo electronico no es valido"
                            else:
                                message = "Error desconocido. Lo sentimos"
                response = {"invited": invited, "message": message, "email": email, "iid": iid, "gravatar": gravatar}
            else:
                response = {"error": "No tienes permiso para hacer eso"}
        else:
            response = "Error invitacion, no puedes entrar desde aqui"
    return HttpResponse(json.dumps(response), mimetype="application/json")


def resendInvitation(request, slug_group):
    if request.is_ajax():
        if request.method == "GET":
            try:
                group = getGroupBySlug(slug_group)
                _user_rel = getRelUserGroup(request.user, group)
                if _user_rel.is_admin and _user_rel.is_active:
                    try:
                        uid = str(request.GET['uid'])
                    except Exception:
                        uid = None
                    if uid == "" or not uid:
                        return HttpResponse(False)
                    _user = getUserById(uid)
                    rel = getRelUserGroup(_user, group)
                    if rel:
                        if not rel.is_active:
                            ctx_email = {
                                "firstname": request.user.first_name,
                                "username": request.user.username,
                                "groupname": group.name,
                                "urlgravatar": showgravatar(request.user.email, 50)
                            }
                            type_email = 11
                            if not _user.is_active:
                                type_email = 10
                                try:
                                    from apps.account.models import activation_keys
                                    ak = activation_keys.objects.get(id_user=_user)
                                    ctx_email["activation_key"] = ak.activation_key
                                    ctx_email["id_inv"] = request.user.pk
                                    ctx_email["newuser_username"] = _user.username
                                    ctx_email["pass"] = ak.activation_key[:8]
                                except Exception, e:
                                    print e
                                    # Error log e
                            message = {"email": _user.email, "sent": True}
                            sendEmailHtml(type_email, ctx_email, [_user.email])  # activate account
                        else:
                            message = {"error": "el usuario ya está activo"}
                    else:
                        message = {"error": "El usuario no pertenece a este grupo", "sent": False}
                else:
                    message = "No tienes permisos para hacer eso."
            except Exception:
                message = False
        else:
            message = False
    else:
        message = False
    return HttpResponse(json.dumps(message), mimetype="application/json")




def changeNames(request, slug_group):
    """
    Cambia los nombres del usuario invitado
    """
    if request.is_ajax():
        if request.method == "GET":
            try:
                group = getGroupBySlug(slug_group)
                _user_rel = getRelUserGroup(request.user, group)
                if _user_rel.is_admin and _user_rel.is_active:
                    error = False
                    try:
                        uid = str(request.GET['uid'])
                    except:
                        uid = None
                    if uid == "" or not uid:
                        return HttpResponse(False)
                    _user = getUserById(uid)
                    try:
                        first_name = request.GET.get('first_name')
                    except:
                        first_name = _user.first_name if _user else ""
                        error = True
                    try:
                        last_name = request.GET.get('last_name')
                    except Exception:
                        last_name = _user.last_name if _user else ""
                        error = True
                    if _user:
                        rel = getRelUserGroup(_user, group)
                        if rel and not error:
                            # change Names
                            _user.first_name = first_name
                            _user.last_name = last_name
                            _user.save()
                            message = {"fname": _user.first_name, "lname": _user.last_name, "changed": True}
                        else:
                            error = "El usuario no pertenece a este grupo" if not rel else "No se pudo editar los nombres."
                            message = {"error": error, "changed": False}
                    else:
                        message = {"error": "No pudes cambiar los nombres de este usuario", "changed": False}
                else:
                    message = "No tienes permisos para hacer eso."
            except Exception:
                message = False
        else:
            message = False
    else:
        message = False
    return HttpResponse(json.dumps(message), mimetype="application/json")


@login_required(login_url='/account/login')
def acceptInvitation(request):
    """
        Acepta invitaciones a grupos
    """
    saveViewsLog(request, "apps.groups_app.views.acceptInvitation")
    noHasPerms = False
    my_response = u"algo pasó y no sabemos si"
    if request.is_ajax():
        if request.method == 'GET':
            try:
                if request.GET['i_id'][0] == 's':
                    accept = True
                else:
                    if request.GET['i_id'][0] == 'n':
                        accept = False
                    else:
                        return HttpResponse(False)  # error 1, peticion sin controlador s o n
                iid = request.GET['i_id'][1:]
                try:
                    inv = rel_user_group.objects.get(id=iid, id_user=request.user, is_active=False)
                    user_from_is_member = True  # isMemberOfGroup(inv.id_user_from, inv.id_group)  # el usuario que lo invito es miembro?
                except invitations_groups.DoesNotExist:
                    inv = False
                    user_from_is_member = False
                if accept and user_from_is_member and inv:  # aprobar la invitacion
                    setUserRoles(inv.id_user, inv.id_group, is_active=1)
                    saveActionLog(request.user, 'SET_INVITA', "id_group: %s, acept: %s, group_name: %s" % (inv.id_group.pk, True, inv.id_group.name), request.META['REMOTE_ADDR'])  # Accion de aceptar invitacion a grupo
                    accepted = True
                    group = {"id": inv.id_group.id, "name": inv.id_group.name, "slug": "/groups/" + inv.id_group.slug, "img_group": inv.id_group.img_group}
                    message = "Aceptar la solicitud"
                    my_response = "Si"
                else:  # no aprobar la invitacion
                    if inv and not accept:
                        inv.is_active = False
                        inv.is_member = False
                        inv.save()
                        if inv.is_superadmin:
                            print "El usuario era superadmin"
                            # En
                        saveActionLog(request.user, 'DEL_INVITA', "id_group: %s, acept: %s, group_name: %s" % (inv.id_group.pk, False, inv.id_group.name), request.META['REMOTE_ADDR'])  # Accion de no aceptar invitacion a grupo
                        accepted = False
                        group = {"id": inv.id_group.id, "name": inv.id_group.name, "slug": "/groups/" + inv.id_group.slug, "img_group": inv.id_group.img_group}
                        message = "NO Aceptar la solicitud"
                        my_response = "No"
                    else:
                        accepted = False
                        message = "El administrador del grupo ha cancelado tu invitaci&oacute;n"
                        group = ""
                        noHasPerms = True
                # send email message
                email_list = []
                email_list.append(str(inv.id_user_invited.email))
                email_ctx = {
                    'firstname': request.user.first_name + " " + request.user.last_name,
                    'username': request.user.username,
                    'response': my_response,
                    'groupname': inv.id_group.name,
                    'groupslug': inv.id_group.slug,
                    'urlgravatar': showgravatar(request.user.email, 50)
                }
                sendEmailHtml(8, email_ctx, email_list, inv.id_group)
                response = {"accepted": accepted, "message": message, "group": group, "canceled": noHasPerms}
            except Exception, e:
                print e
                return HttpResponse(False)
    else:
        response = "Error invitacion is not AJAX"
    return HttpResponse(json.dumps(response), mimetype="application/json")


@login_required(login_url='/account/login')
def deleteInvitation(request, slug_group):
    saveViewsLog(request, "apps.groups_app.views.deleteInvitation")
    if request.is_ajax():
        if request.method == 'GET':
            group = getGroupBySlug(slug_group)
            _user_rel = getRelUserGroup(request.user, group)
            if _user_rel.is_admin and _user_rel.is_active:
                try:
                    iid = request.GET['id_inv']
                    if iid == "" or not iid:
                        return HttpResponse(False)
                    _user = getUserById(iid)
                    rel = getRelUserGroup(_user, group)
                    if rel:
                        saveActionLog(
                            request.user, 'DEL_INVITA',
                            "user: %s, grupo: %s, id_user_invited=%s,  is_superadmin=%s, is_admin=%s, is_secretary=%s, is_member=%s, is_active=%s, is_convener=%s, date_joined=%s" % (_user, group, rel.id_user_invited, rel.is_superadmin, rel.is_admin, rel.is_secretary, rel.is_member, rel.is_active, rel.is_convener, rel.date_joined),
                            request.META['REMOTE_ADDR'])  # Accion de eliminar invitaciones
                        rel.delete()
                        deleted = True
                        message = "El usuario (" + _user.username + ") ya no podr&aacute; acceder a este grupo"
                        response = {"deleted": deleted, "message": message}
                    else:
                        response = "Error de relación"
                except Exception, e:
                    print "error ", e
                    return HttpResponse(False)
            else:
                response = "No tienes permisos para hacer eso."
        if request.method == 'POST':
            response = "Error invitacion"
    else:
        response = "Error invitacion"
    return HttpResponse(json.dumps(response), mimetype="application/json")


def getGroupBySlug(slug):
    try:
        group = groups.objects.get(slug=slug, is_active=True)
    except groups.DoesNotExist:
        group = None
        raise Http404
    except Exception, e:
        group = None
        raise Http404
        print "Error capturando grupo: %s " % e
    return group


@login_required(login_url='/account/login')
def newReunion(request, slug):
    saveViewsLog(request, "apps.groups_app.views.newReunion")
    q = groups.objects.get(slug=slug, is_active=True)
    is_member = rel_user_group.objects.filter(id_group=q.id, id_user=request.user)
    if is_member:
        if request.method == "POST":
            form = newReunionForm(request.POST)
            if form.is_valid():
                df = {
                    'date_reunion': form.cleaned_data['date_reunion'],
                    'title': form.cleaned_data['title'],
                    'locale': form.cleaned_data['locale'],
                    'agenda': form.cleaned_data['agenda'],
                }
                myNewReunion = reunions(
                    id_convener=request.user,
                    date_reunion=df['date_reunion'],
                    title=df['title'],
                    locale=df['locale'],
                    id_group=q,
                    agenda=df['agenda'],
                )
                myNewReunion.save()
                id_reunion = myNewReunion
                relations = rel_user_group.objects.filter(id_group=q, is_active=1)
                email_list = []
                for relation in relations:
                    email_list.append(str(relation.id_user.email)) # bug found at 25,07,2013
                email_ctx = {
                    'firstname': request.user.first_name,
                    'username': request.user.username,
                    'groupname': q.name,
                    'titlereunion': str(df['title'].encode('utf8', 'replace')),
                    'datereunion': dateTimeFormatForm(df['date_reunion']),
                    'locale': str(df['locale'].encode('utf8', 'replace')),
                    'agenda': str(df['agenda'].encode('utf8', 'replace')),
                    'datereunionshort': str(datetime.datetime.strftime(make_naive(df['date_reunion'], get_default_timezone()), "%Y-%m-%d")),
                    'id_reunion': id_reunion.pk,
                    'urlgravatar': showgravatar(request.user.email, 50)
                }
                sendEmailHtml(2, email_ctx, email_list, q)
                saveActionLog(request.user, 'NEW_REUNION', "Title: %s id_reunion: %s grupo: %s" % (df['title'], id_reunion.pk, q.name), request.META['REMOTE_ADDR'])  # Guardar accion de crear reunion
                return HttpResponseRedirect("/groups/calendar/" + str(datetime.datetime.strftime(make_naive(df['date_reunion'], get_default_timezone()), "%Y-%m-%d")) + "?r=" + str(id_reunion.pk))

        else:
            form = newReunionForm()
        ctx = {'TITLE': "Actarium",
               "newReunionForm": form,
               "group": q
               }
        return render_to_response('groups/newReunion.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/groups/#error-view-group')


@login_required(login_url='/account/login')
def calendar(request):
    saveViewsLog(request, "apps.groups_app.views.calendar")
    gr = groups.objects.filter(rel_user_group__id_user=request.user)  # grupos
    my_reu = reunions.objects.filter(id_group__in=gr, is_done=False).order_by("-date_convened")  # reuniones
    my_reu_day = reunions.objects.filter(id_group__in=gr).order_by("-date_convened")  # reuniones para un dia
    i = 0
    json_array = {}
    for reunion in my_reu_day:
        td = make_naive(reunion.date_reunion, get_default_timezone()) - datetime.datetime.now()
        if not(td.days >= 0 and td.seconds >= 0 and td.microseconds >= 0):
            is_last = 1
        else:
            is_last = 0
        try:
            confirm = assistance.objects.get(id_user=request.user, id_reunion=reunion.pk)
            is_confirmed = confirm.is_confirmed
            is_saved = 1
        except assistance.DoesNotExist:
            is_confirmed = False
            is_saved = 0
        json_array[i] = {"id_r": str(reunion.id),
                         "group_slug": reunion.id_group.slug,
                         "group_name": reunion.id_group.name,
                         "date": humanize.naturaltime(reunion.date_reunion),
                         "date_normal": dateTimeFormatForm(reunion.date_reunion),
                         'is_confirmed': str(is_confirmed),
                         'is_saved': is_saved,
                         "title": reunion.title,
                         'is_last': is_last}
        i = i + 1
    response = json_array
    ctx = {
        "reunions_day": my_reu,
        "reunions": my_reu,
        "my_reu_day_json": json.dumps(response),
        "groups": gr}
    return render_to_response('groups/calendar.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def calendarDate(request, slug=None):
    saveViewsLog(request, "apps.groups_app.views.calendarDate")
    gr = groups.objects.filter(rel_user_group__id_user=request.user)  # grupos
    my_reu = reunions.objects.filter(id_group__in=gr, is_done=False).order_by("-date_convened")  # reuniones
    dateslug_min = str(make_aware(datetime.datetime.strptime(slug + " 00:00:00", '%Y-%m-%d %H:%M:%S'), get_default_timezone()))
    dateslug_max = str(make_aware(datetime.datetime.strptime(slug + " 23:59:59", '%Y-%m-%d %H:%M:%S'), get_default_timezone()))
    my_reu_day = reunions.objects.filter(id_group__in=gr, date_reunion__range=[dateslug_min, dateslug_max]).order_by("-date_convened")  # reuniones para un dia
    i = 0
    json_array = {}
    for reunion in my_reu_day:
        td = make_naive(reunion.date_reunion, get_default_timezone()) - datetime.datetime.now()
        if not(td.days >= 0 and td.seconds >= 0 and td.microseconds >= 0):
            is_last = 1
        else:
            is_last = 0
        try:
            confirm = assistance.objects.get(id_user=request.user, id_reunion=reunion.pk)
            is_confirmed = confirm.is_confirmed
            is_saved = 1
        except assistance.DoesNotExist:
            is_confirmed = False
            is_saved = 0
        json_array[i] = {"id_r": str(reunion.id),
                         "group_slug": reunion.id_group.slug,
                         "group_name": reunion.id_group.name,
                         "date": humanize.naturaltime(reunion.date_reunion),
                         "date_normal": dateTimeFormatForm(reunion.date_reunion),
                         'is_confirmed': str(is_confirmed),
                         'is_saved': is_saved,
                         'title': reunion.title,
                         'is_last': is_last}
        i = i + 1
    response = json_array
    ctx = {
        "reunions_day": my_reu_day,
        "reunions": my_reu,
        "my_reu_day_json": json.dumps(response),
        "groups": gr}
    return render_to_response('groups/calendar.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def getReunions(request):
    saveViewsLog(request, "apps.groups_app.views.getReunions")
    if request.is_ajax():
        if request.method == 'GET':
            date = str(request.GET['date'])
            gr = groups.objects.filter(rel_user_group__id_user=request.user)  # grupos
            dateslug_min = str(make_aware(datetime.datetime.strptime(date + " 00:00:00", '%Y-%m-%d %H:%M:%S'), get_default_timezone()))
            dateslug_max = str(make_aware(datetime.datetime.strptime(date + " 23:59:59", '%Y-%m-%d %H:%M:%S'), get_default_timezone()))
            my_reu_day = reunions.objects.filter(id_group__in=gr, date_reunion__range=[dateslug_min, dateslug_max]).order_by("-date_convened")  # reuniones para un dia
            i = 0
            json_array = {}
            for reunion in my_reu_day:
                td = make_naive(reunion.date_reunion, get_default_timezone()) - datetime.datetime.now()
                if not(td.days >= 0 and td.seconds >= 0 and td.microseconds >= 0):
                    is_last = 1
                else:
                    is_last = 0
                try:
                    confirm = assistance.objects.get(id_user=request.user, id_reunion=reunion.pk)
                    is_confirmed = confirm.is_confirmed
                    is_saved = 1
                except assistance.DoesNotExist:
                    is_confirmed = False
                    is_saved = 0
                json_array[i] = {"id_r": str(reunion.id),
                                 "group_slug": reunion.id_group.slug,
                                 "group_name": reunion.id_group.name,
                                 "date": humanize.naturaltime(reunion.date_reunion),
                                 "date_normal": dateTimeFormatForm(reunion.date_reunion),
                                 'is_confirmed': is_confirmed,
                                 'is_saved': is_saved,
                                 "title": reunion.title,
                                 "is_last": is_last}
                i = i + 1
            response = json_array
    else:
        response = "Error Calendar"
    return HttpResponse(json.dumps(response), mimetype="application/json")


@login_required(login_url='/account/login')
def getNextReunions(request):
    """
        Se muestra debajo del calendario las proximas 3 reuniones a las cuales ya ha sido confirmada la asistencia.
    """
    saveViewsLog(request, "apps.groups_app.views.getNextReunions")
    if request.is_ajax():
        gr = groups.objects.filter(rel_user_group__id_user=request.user)  # grupos
        my_reu_day = reunions.objects.filter(id_group__in=gr, date_reunion__gt=datetime.date.today()).order_by("date_reunion")  # reuniones para un dia
        i = 0
        json_array = {}
        for reunion in my_reu_day:
            if(i < 3):
                try:
                    confirm = assistance.objects.get(id_user=request.user, id_reunion=reunion.pk)
                    is_confirmed = confirm.is_confirmed
                    is_saved = 1
                    if (is_confirmed):
                        json_array[i] = {"id_r": str(reunion.id),
                                         "group_slug": reunion.id_group.slug,
                                         "group_name": reunion.id_group.name,
                                         "date": humanize.naturaltime(reunion.date_reunion),
                                         "date_normal": dateTimeFormatForm(reunion.date_reunion),
                                         'is_confirmed': is_confirmed,
                                         'is_saved': is_saved,
                                         "title": reunion.title}
                        i = i + 1
                except assistance.DoesNotExist:
                    is_confirmed = False
                    is_saved = 0
        response = json_array
        # print json_array
    else:
        response = "Error Calendar"
    return HttpResponse(json.dumps(response), mimetype="application/json")


def getAssistance(id_minutes):
    try:
        assistan = assistance.objects.filter(id_minutes=id_minutes)
    except Exception, e:
        raise e
        assistan = False
    return assistan


@login_required(login_url='/account/login')
def setAssistance(request):
    saveViewsLog(request, "apps.groups_app.views.setAssistance")
    if request.is_ajax():
        if request.method == 'GET':
            id_reunion = reunions.objects.get(pk=request.GET['id_reunion'])
            id_user = request.user
            is_confirmed = str(request.GET['is_confirmed'])
            if (is_confirmed == "true"):
                is_confirmed = True
                resp = u"Si asistirá"
            else:
                is_confirmed = False
                resp = u"No asistirá"
            assis, created = assistance.objects.get_or_create(id_user=id_user, id_reunion=id_reunion)
    #        if created:
    #            assis = assistance.objects.get(id_user=id_user, id_reunion=id_reunion)
            assis.is_confirmed = is_confirmed
    #        assis.is_confirmed = is_confirmed
            assis.save()
            email_list = []
            email_list.append(str(id_reunion.id_convener.email))
            ctx_email = {
                'firstname': request.user.first_name,
                'username': request.user.username,
                'response': resp,
                'groupname': id_reunion.id_group.name,
                'titlereunion':  id_reunion.title,
                'datereunion': id_reunion.date_reunion,
                'idreunion': id_reunion.pk,
                'urlgravatar': showgravatar(request.user.email, 50)
            }
            saveActionLog(id_user, 'SET_ASSIST', "id_reunion: %s, is_confirmed: %s" % (id_reunion.pk, is_confirmed), request.META['REMOTE_ADDR'])
            datos = "id_reunion = %s , id_user = %s , is_confirmed = %s, created %s" % (id_reunion.pk, id_user, is_confirmed, created)
            sendEmailHtml(5, ctx_email, email_list, id_reunion.id_group)
        return HttpResponse(json.dumps(datos), mimetype="application/json")
    else:
        response = "Error Calendar"
        return HttpResponse(json.dumps(response), mimetype="application/json")


@login_required(login_url='/account/login')
def getReunionData(request):
    saveViewsLog(request, "apps.groups_app.views.getReunionData")
    if request.is_ajax():
        if request.method == 'GET':
            id_reunion = str(request.GET['id_reunion'])
            reunion = reunions.objects.get(pk=id_reunion)
            convener = reunion.id_convener.first_name + " " + reunion.id_convener.last_name + " (" + reunion.id_convener.username + ")"
            date_convened = reunion.date_convened
            date_convened = removeGMT(date_convened)
            date_reunion = reunion.date_reunion
            date_reunion = removeGMT(date_reunion)
            locale = reunion.locale
            title = reunion.title
            group = reunion.id_group.name
            id_group = reunion.id_group
            agenda = reunion.agenda
            is_done = reunion.is_done
            group_slug = reunion.id_group.slug
            assistants = rel_user_group.objects.filter(id_group=id_group)
            assis_list = {}
            hM = reunion.hasMinutes()
            i = 0
            c = 0
            for assistant in assistants:
                try:
                    confirm = assistance.objects.get(id_user=assistant.id_user, id_reunion=reunion.pk)
                    is_confirmed = confirm.is_confirmed
                    is_saved = 1
                except assistance.DoesNotExist:
                    is_confirmed = False
                    is_saved = 0
                if is_saved == 1:
                    if is_confirmed:  # reuniones confirmadas
                        c = "Asistir&aacute;"
                    else:  # reuniones rechazadas
                        c = "No asistir&aacute;"
                else:  # reuniones pendientes por confirmar
                    c = "Sin responder"
                assis_list[i] = {'username': assistant.id_user.first_name + " (" + assistant.id_user.username + ")", "is_confirmed": c, "gravatar": showgravatar(assistant.id_user.email, 30)}
                i = i + 1
            iconf = 0
            try:
                my_confirm = assistance.objects.get(id_user=request.user, id_reunion=reunion.pk)
                my_confirmation = my_confirm.is_confirmed
                if my_confirmation:
                    iconf = 1
                else:
                    if not my_confirmation:
                        iconf = 2
            except assistance.DoesNotExist:
                    iconf = 3
            if hM:
                has_minute = 1
                minute_code = reunion.getMinutes().code
            else:
                has_minute = 0
                minute_code = 0
            reunion_data = {
                "convener": convener,
                "date_convened": str(dateTimeFormatDb(date_convened)),
                "date_reunion": str(dateTimeFormatDb(date_reunion)),
                "group": group,
                "agenda": agenda,
                "locale": locale,
                "title": title,
                "is_done": is_done,
                "assistants": assis_list,
                "group_slug": group_slug,
                "iconf": iconf,
                "has_minute": has_minute,
                "minute_code": minute_code
            }
    else:
        reunion_data = "Error Calendar"
    return HttpResponse(json.dumps(reunion_data), mimetype="application/json")


def dateTimeFormatForm(datetime_var):
    return str(datetime.datetime.strftime(make_naive(datetime_var, get_default_timezone()), "%d de %B de %Y a las %I:%M %p"))


def dateTimeFormatDb(datetime_var):
    UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now()
    local_datetime = datetime.datetime.strptime(str(datetime_var), "%Y-%m-%d %H:%M:%S")
    result_utc_datetime = local_datetime - UTC_OFFSET_TIMEDELTA
    return str(result_utc_datetime.strftime("%d de %B de %Y a las %I:%M %p"))


def removeGMT(datetime_var):
    dt = str(datetime_var)
    dt_s = dt[:19]
    return str(datetime.datetime.strptime("%s" % (dt_s), "%Y-%m-%d %H:%M:%S"))
