# Create your views here.
#encoding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.http import Http404
from groups.models import *
from groups.forms import newGroupForm, newMinutesForm, newReunionForm, uploadMinutesForm
from django.contrib.auth.models import User
import datetime
from django.utils.timezone import make_aware, get_default_timezone, make_naive
from django.utils import simplejson as json
from account.templatetags.gravatartag import showgravatar
from actions_log.views import saveActionLog
from Actarium.settings import URL_BASE
from emailmodule.views import sendEmailHtml
from groups.validators import validateEmail


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


def getUserByEmail(email):
    try:
        _user = User.objects.get(email=email)
        return _user
    except User.DoesNotExist:
        return None


@login_required(login_url='/account/login')
def groupsList(request):
    '''
    lista los grupos del usuario registrado
    '''
    try:
        mygroups = rel_user_group.objects.filter(id_user=request.user, is_active=True, is_member=True).order_by("date_joined")
        my_admin_groups = rel_user_group.objects.filter(
            id_user=request.user,
            is_member=False,
            is_active=True,
            is_admin=True).order_by("date_joined")
    except rel_user_group.DoesNotExist:
        mygroups = "You Dont have any groups"
        my_admin_groups = "You Dont administrate any groups"

    ctx = {"groups": mygroups, "admin_groups": my_admin_groups}
    return render_to_response('groups/groupsList.html', ctx, context_instance=RequestContext(request))


def removeUniqueRolGroup(group, role):
    try:
        if role == 4:
            r = rol_user_minutes.objects.get(id_group=group, is_president=True, is_active=False)
            r.is_president = False
        if role == 5:
            r = rol_user_minutes.objects.get(id_group=group, is_secretary=True, is_active=False)
            r.is_secretary = False
        r.save()
        return True
    except rol_user_minutes.DoesNotExist:
        return True
    except Exception:
        return False


@login_required(login_url='/account/login')
def setRolForMinute(request, slug_group):
    """
        Set or remove role to a user
        Roles id:
            1 = Signer
            2 = Approver
            3 = Assistance
            4 = President
            5 = Secretary
    """
    r1, r2, r3, r4, r5 = "Firmador", "Aprobador", "Asistente", "Presidente", "Secretario"
    error = None
    saved = True
    role_name = ""
    if request.is_ajax():
        if request.method == 'GET':
            try:
                g = getGroupBySlug(slug=slug_group)
                _user_rel = getRelUserGroup(request.user, g)

                if _user_rel.is_secretary:
                    role = int(request.GET['role'])
                    remove = bool(int(request.GET['remove']))
                    _user = get_user_or_email(request.GET['uid'])
                    u = _user['user']
                    if u:
                        rel = getRolUserMinutes(u, g)
                    if not rel:
                        rel = setRolUserMinutes(u, g)
                        if rel:
                            rel = getRolUserMinutes(u, g)
                        else:
                            rel = False
                    if rel:
                        if role == 1 and u and not remove:
                            rel.is_signer = True
                            role_name = r1
                        if role == 2 and u and not remove:
                            rel.is_approver = True
                            role_name = r2
                        if role == 3 and u and not remove:
                            rel.is_assistant = True
                            role_name = r3
                        if role == 4 and u and not remove:
                            if removeUniqueRolGroup(g, 4):
                                rel.is_president = True
                            role_name = r4
                        if role == 5 and u and not remove:
                            if removeUniqueRolGroup(g, 5):
                                rel.is_secretary = True
                            role_name = r5

                        if role == 1 and u and remove:
                            rel.is_signer = False
                        if role == 2 and u and remove:
                            rel.is_approver = False
                        if role == 3 and u and remove:
                            rel.is_assistant = False

                        # esto sobra
                        # if role == 4 and u and remove:
                        #     rel.is_president = False
                        # if role == 5 and u and remove:
                        #     rel.is_secretary = False

                        rel.save()
                        saved = True
                        # saveAction added Rol: group: g, user: u, role = role, role name=role_name, set or remove?: remove
                else:
                    error = "No tienes permiso para hacer eso, Por favor recarga la p&aacute;gina"
            except groups.DoesNotExist:
                error = "Este grupo no existe"
            except rol_user_minutes.DoesNotExist:
                error = "Error! no existe el usuario para esta acta"
            except Exception, e:
                print e
                error = "Por favor recarga la p&aacute;gina e intenta de nuevo."
            if error:
                return HttpResponse(json.dumps({"error": error, "saved": False}), mimetype="application/json")
            response = {"saved": saved, "u": u.first_name, "role": role_name}
            return HttpResponse(json.dumps(response), mimetype="application/json")
    return HttpResponse(json.dumps({"error": "You can not enter here"}), mimetype="application/json")


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
            sendEmailHtml(4, ctx_email, [rel.id_user.email])
        return True
    return False


def setRole(request, slug_group):
    """
        Set or remove role to a user
    """
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
            except Exception, e:
                print e
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


def setUserRoles(_user, _group, is_superadmin=0, is_admin=0, is_approver=0, is_secretary=0, is_member=1, is_active=True):
    try:
        no_rel = False
        relation = getRelUserGroup(_user, _group)
        if relation:
            relation.is_member = bool(is_member)
            if is_superadmin:
                relation.is_superadmin = bool(is_superadmin)
            if is_admin:
                relation.is_admin = bool(is_admin)
            if is_secretary:
                relation.is_secretary = bool(is_secretary)
            if is_approver:
                relation.is_approver
            if is_active:
                relation.is_active = bool(is_active)
            relation.save()
        else:
            no_rel = True
    except rel_user_group.DoesNotExist:
        no_rel = True
    if no_rel:
        setRelUserGroup(id_user=_user, id_group=_group, is_member=bool(is_member), is_active=is_active, is_admin=is_admin, is_approver=is_approver, is_secretary=is_secretary, is_superadmin=is_superadmin)


def get_user_or_email(s):
    if validateEmail(s):
        return {"user": False, "email": str(s)}
    else:
        try:
            if isinstance(int(s), int):  # valida si es un entero
                _user = User.objects.get(id=int(s))
                return {"user": _user, "email": str(s)}
        except User.DoesNotExist:
            return {"user": False, "email": str(s)}
        except Exception:
            return {"user": False, "email": False}


@login_required(login_url='/account/login')
def newBasicGroup(request, form, pro=False):
    df = {
        'name': form.cleaned_data['name'],
        'description': form.cleaned_data['description'],
        'id_creator': request.user,
        # 'id_group_type': form.cleaned_data['id_group_type']  # Se omite para no pedir tipo de grupo
        'id_group_type': 1
    }
    myNewGroup = groups(name=df['name'],
                       description=df['description'],
                       id_creator=df['id_creator'],
                       id_group_type=group_type.objects.get(pk=df['id_group_type']),
                     )
    myNewGroup.save()
    if not pro:  # new rel to: Create free group
        setRelUserGroup(id_user=request.user, id_group=myNewGroup, is_superadmin=1, is_admin=1, is_active=True)
    else:
        try:
            user_or_email = get_user_or_email(request.POST['id_admin'])
            print user_or_email
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
    # print "type-group: %s , id-organization: %s, id-billing: %s" % (request.POST['type-group'], request.POST['sel-organization'], request.POST['sel-billing'])
    try:
        org = organizations.objects.get(id=request.POST['sel-organization'], id_admin=request.user, is_active=True)
    except Exception:
        org = False
    try:
        bill = billing.objects.get(id=request.POST['sel-billing'], id_user=request.user, state='1')
    except Exception:
        bill = False
    if org and bill:
        # crear pro
        new_group = newBasicGroup(request, form, pro=True)
        g_pro = groups_pro(id_group=new_group, id_organization=org, id_billing=bill)
        g_pro.save()
        # consumir package
        return new_group
    else:
        return False


@login_required(login_url='/account/login')
def getProGroupDataForm(request):
    orgs = None
    billing_list = None
    try:
        orgs = organizations.objects.filter(is_active=True, id_admin=request.user)
    except Exception, e:
        orgs = None
        raise e
    try:
        billing_list = billing.objects.filter(state='1', id_user=request.user)
    except billing.DoesNotExist:
        billing_list = "No hay información disponible."
    return (orgs, billing_list)


@login_required(login_url='/account/login')
def newGroup(request):
    '''
        crea una nuevo grupo
    '''
    orgs = None
    billing_list = None
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
                # Guardar accion de crear reunion
                saveActionLog(request.user, 'NEW_GROUP', "id_group: %s, group_name: %s, admin: %s" % (resp.pk, resp.name, request.user.username), request.META['REMOTE_ADDR'])
                return HttpResponseRedirect("/groups/" + str(resp.slug) + "?saved=1")
    else:
        form = newGroupForm()
    orgs, billing_list = getProGroupDataForm(request)
    ctx = {"newGroupForm": form,
           "organizations": orgs,
           "billing": billing_list,
           "sel_org": sel_org,
           "full_path": request.get_full_path()
           }
    return render_to_response('groups/newGroup.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def showGroup(request, slug):
    '''
        Muestra la informacion de un grupo
    '''
    try:
        g = groups.objects.get(slug=slug, is_active=True)
        _user = getRelUserGroup(request.user, g)
        if _user:
            if _user.is_active:
                members = rel_user_group.objects.filter(id_group=g.id, is_member=True).order_by("-is_active")
                minutes_group = minutes.objects.filter(id_group=g.id, is_valid=True).order_by("-id")
                _reunions = reunions.objects.filter(id_group=g).order_by("date_reunion")
                if request.method == "GET":
                    try:
                        no_redactor = request.GET['no_redactor']
                    except Exception:
                        no_redactor = 0
                ctx = {"group": g, "current_member": _user, "members": members, "minutes": minutes_group, "reunions": _reunions, "now_": datetime.datetime.now(), 'no_redactor': no_redactor}
                return render_to_response('groups/showGroup.html', ctx, context_instance=RequestContext(request))
            if _user.is_admin and _user.is_active:
                return HttpResponseRedirect('/groups/' + str(g.slug) + "/admin")
            if _user.is_superadmin and _user.is_active:
                return HttpResponseRedirect("/settings/organizations")
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
        print "groups Exception ", slug
        raise Http404
    except rel_user_group.DoesNotExist:
        print "rel_user_group Exception ", slug
        raise Http404


@login_required(login_url='/account/login')
def getMembers(request):
    if request.is_ajax():
        if request.method == "GET":
            try:
                search = str(request.GET['search'])
                if validateEmail(search):
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
                        "mail": ans.email,
                        "gravatar": showgravatar(ans.email, 20)}
                else:
                    if ans == 1:  # email valido, pero no es usuario
                        message = {"user_id": search, "mail_is_valid": True,
                                    "mail": search, "username": False,
                                    "gravatar": showgravatar(search, 20)}
                    else:
                        if ans == 2:  # no existe el usuario
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


def sendInvitationToGroup(id_user_invited, id_user_from, group):
    '''
        Enviar una invitacion de grupo a un usuario
    '''
    try:
        _inv = setRelUserGroup(id_user=id_user_invited, id_group=group, is_member=True, is_active=False)
    except Exception, e:
        print e
        return False
    if _inv:
        email = [id_user_invited.email]
        ctx_email = {
             'firstname': id_user_from.first_name + id_user_from.last_name,
             'username': id_user_from.username,
             'groupname': group.name,
             'urlgravatar': showgravatar(id_user_from.email, 50)
         }
        sendEmailHtml(6, ctx_email, email)
    return _inv


def newUserWithInvitation(email, id_user_from, group):
    '''
        Crear un nuevo usuario y lo relaciona al grupo.
    '''
    if validateEmail(email):
        try:
            if not getUserByEmail(email):
                from account.views import newInvitedUser
                _user = newInvitedUser(email, id_user_from)
                if _user:
                    return _user
                else:
                    return False
            else:
                return False
        except Exception, e:
            print e
        return False
    else:
        return 0  # Email Failed


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
    if request.is_ajax():
        if request.method == 'GET':
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
                print "se esta agregando"
                email = str(request.GET['mail'])
                if isMemberOfGroupByEmail(email, g):
                    invited = False
                    message = "El usuario ya es miembro del grupo"
                    print message
                    iid = False
                    gravatar = False
                else:
                    _user = getUserByEmail(email)
                    if not _user:
                        _user = newUserWithInvitation(email, request.user, g)
                    sendInvitationToGroup(_user, request.user, g)
                    if _user and not (_user is 0):  # 0 = is email failed
                        try:
                            invited = True
                            iid = str(_user.id)  # get de id from invitation
                            gravatar = showgravatar(email, 30)
                            message = "Se ha enviado la invitación a " + str(email) + " al grupo <strong>" + g.name + "</strong>"
                            saveActionLog(request.user, 'SET_INVITA', "email: %s" % (email), request.META['REMOTE_ADDR'])  # Accion de aceptar invitacion a grupo
                        except Exception, e:
                            print e
                    else:
                        iid = False
                        invited = False
                        gravatar = False
                        if not _user and not (_user is 0):
                            message = "El email que estas tratando de registrar ya tiene una cuenta."
                            # message = "El usuario tiene la invitación pendiente"
                        else:
                            if _user == 0:
                                message = "El correo electronico no es valido"
                            else:
                                message = "Error desconocido. Lo sentimos"
                response = {"invited": invited, "message": message, "email": email, "iid": iid, "gravatar": gravatar}
            else:
                print "no se agregó:", _user_rel
                response = {"error": "No tienes permiso para hacer eso"}
        else:
            response = "Error invitacion, no puedes entrar desde aqui"
    return HttpResponse(json.dumps(response), mimetype="application/json")


def getRelUserGroup(_user, _group):
    try:
        return rel_user_group.objects.get(id_user=_user, id_group=_group)
    except rel_user_group.DoesNotExist:
        return False
    except Exception:
        return False


def setRelUserGroup(id_user, id_group,
    is_superadmin=False,
    is_admin=False,
    is_approver=False,
    is_secretary=False,
    is_member=True,
    is_active=False):
    try:
        rel = rel_user_group(
            id_user=id_user,
            id_group=id_group,
            is_member=bool(is_member),
            is_admin=is_admin,
            is_approver=is_approver,
            is_secretary=is_secretary,
            is_superadmin=is_superadmin,
            is_active=is_active)
        rel.save()
        # saveAction new Rel user group
        return True
    except Exception:
        # error log
        return False


def getRolUserMinutes(_user, id_group, id_minutes=None):
    try:
        return rol_user_minutes.objects.get(id_user=_user, id_group=id_group, id_minutes=id_minutes)
    except rol_user_minutes.DoesNotExist:
        return False
    except Exception:
        print "getRolUserMinutes Error"
        return False


def setRolUserMinutes(id_user, id_group,
    id_minutes=None,
    is_president=False,
    is_approver=False,
    is_secretary=False,
    is_assistant=False,
    is_signer=False,
    is_active=False):
    try:
        rel = rol_user_minutes(
            id_user=id_user,
            id_group=id_group,
            id_minutes=id_minutes,
            is_president=is_president,
            is_approver=is_approver,
            is_secretary=is_secretary,
            is_assistant=is_assistant,
            is_signer=is_signer,
            is_active=is_active)
        rel.save()
        # saveAction new Rol user minutes
        return True
    except Exception, e:
        print "erroooor:", e
        # error log
        return False


@login_required(login_url='/account/login')
def acceptInvitation(request):
    """
        Acepta invitaciones a grupos
    """
    noHasPerms = False
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
                    else:
                        accepted = False
                        message = "El administrador del grupo ha cancelado tu invitaci&oacute;n"
                        group = ""
                        noHasPerms = True
                response = {"accepted": accepted, "message": message, "group": group, "canceled": noHasPerms}
            except Exception, e:
                print e
                return HttpResponse(False)
    else:
        response = "Error invitacion is not AJAX"
    return HttpResponse(json.dumps(response), mimetype="application/json")


@login_required(login_url='/account/login')
def deleteInvitation(request):
    if request.is_ajax():
        if request.method == 'GET':
            try:
                iid = request.GET['id_inv']
                if iid == "" or iid == None:
                    return HttpResponse(False)
                try:
                    inv = invitations_groups.objects.get(id=iid, is_active=True)
                except invitations_groups.DoesNotExist:
                    inv = False
                    print "inv ", inv
                if inv:  # si eliminar la invitacion
                    inv.is_active = False
                    print "iid ", iid
                    inv.save()
                    saveActionLog(request.user, 'DEL_INVITA', "id_invitacion: %s, grupo: %s, email_invited: %s" % (iid, inv.id_group.name, inv.id_user_invited.email), request.META['REMOTE_ADDR'])  # Accion de eliminar invitaciones
                    deleted = True
                    message = "El usuario (" + inv.id_user_invited.username + ") ya no podr&aacute; acceder a este grupo"
                    response = {"deleted": deleted, "message": message}
                else:  # no eliminar la invitacion
                    return HttpResponse(inv)
            except Exception, e:
                print "error ", e
                return HttpResponse(False)
        if request.method == 'POST':
            print "POST"
    else:
        response = "Error invitacion"
    return HttpResponse(json.dumps(response), mimetype="application/json")


def getMembersSigned(group, minutes_current):
    try:
        members_signed = rel_user_minutes_assistance.objects.filter(id_minutes=minutes_current)
    except rel_user_minutes_assistance.DoesNotExist:
        members_signed = False
    except Exception, e:
        print "Error getMembersSigned: %s " % e
        members_signed = False
    return members_signed


def getMinutesById(minutes_id):
    try:
        the_minutes = minutes.objects.get(id=minutes_id)
    except minutes.DoesNotExist:
        the_minutes = False
    except Exception, e:
        print "Error getMinutesById: %s" % e
        the_minutes = False
    return the_minutes


def getMinutesByCode(group, code_id):
    try:
        minutes_current = minutes.objects.get(id_group=group, code=code_id)
    except minutes.DoesNotExist:
        minutes_current = False
    except Exception, e:
        print "Error getMinutesByCode: %s" % e
        minutes_current = False
    return minutes_current


def getPrevNextOfGroup(group, minutes_id):
    prev = None
    next = None
    try:
        prev = minutes.get_previous_by_date_created(minutes_id, id_group=group)
    except minutes.DoesNotExist:
        prev = False
    except Exception, e:
        print "Exception prev: " + str(e)
    try:
        next = minutes.get_next_by_date_created(minutes_id, id_group=group)
    except minutes.DoesNotExist:
        next = False
    except Exception, e:
        print "Exception next: " + str(e)
    return prev, next


def getGroupBySlug(slug):
    try:
        group = groups.objects.get(slug=slug, is_active=True)
    except groups.DoesNotExist:
        group = False
        raise Http404
    except Exception, e:
        group = False
        raise Http404
        print "Error capturando grupo: %s " % e
    return group


def getMembersAssistance(group, minutes_current):
    try:
        selected = rel_user_minutes_assistance.objects.filter(id_minutes=minutes_current, assistance=True)
        no_selected = rel_user_minutes_assistance.objects.filter(id_minutes=minutes_current, assistance=False)
        return (selected, no_selected)
    except Exception, e:
        print e
        return None


@login_required(login_url='/account/login')
def showMinutes(request, slug, minutes_code):
    '''
    Muestra toda la informacion de un Acta (minutes)
    '''
    pdf_address = 'false'
    if request.method == 'POST':
        html_data = request.POST['minutes-html-data']
        from pdfmodule.views import minutesHtmlToPdf
        pdf_address = minutesHtmlToPdf(html_data)
        return HttpResponseRedirect(pdf_address)
    group = getGroupBySlug(slug)
    if not group:
        return HttpResponseRedirect('/groups/#error-there-is-not-the-group')

    if isMemberOfGroup(request.user, group):
        minutes_current = getMinutesByCode(group, minutes_code)
        address_template = minutes_current.id_template.address_template
        try:
            data = minutes_type_1.objects.get(id=minutes_current.id_extra_minutes)
        except minutes_type_1.DoesNotExist:
            data = None
        list_newMinutesForm = {
            "date_start": data.date_start,
            "date_end": data.date_end,
            "location": data.location,
            "agreement": data.agreement,
            "agenda": data.agenda,
            "type_reunion": data.type_reunion,
            "code": minutes_current.code
            }
        if not minutes_current:
            return HttpResponseRedirect('/groups/' + slug + '/#error-there-is-not-that-minutes')

        ######## <ASISTENTES> #########
        m_assistance, m_no_assistance = getMembersAssistance(group, minutes_current)
        ######## <ASISTENTES> #########

        ######## <ATTENDING> #########
        try:
            my_attending = getRolUserMinutes(request.user, group, id_minutes=minutes_current)

            my_attending = my_attending.is_approver
        except Exception, e:
            print e
            my_attending = False
        ######## </ATTENDING> #########

        ######## <APPROVED LISTS> #########
        try:
            missing_approved_list = rel_user_minutes_assistance.objects.filter(id_minutes=minutes_current, assistance=0)
            missing_approved_list = 0 if len(missing_approved_list) == 0 else missing_approved_list
        except rel_user_minutes_assistance.DoesNotExist:
            print "NO HAY rel_user_minutes_assistance missing_approved_list"
        except Exception, e:
            print "error,", e

        approved_list = None
        no_approved_list = None
        try:
            approved_list = rel_user_minutes_assistance.objects.filter(id_minutes=minutes_current, assistance=1)
            approved_list = 0 if len(approved_list) == 0 else approved_list
        except rel_user_minutes_assistance.DoesNotExist:
            print "NO HAY rel_user_minutes_assistance APPROVED_LIST"
        except Exception, e:
            print "Error APPROVED_LIST,", e
        try:
            no_approved_list = rel_user_minutes_assistance.objects.filter(id_minutes=minutes_current, assistance=2)
            no_approved_list = 0 if len(no_approved_list) == 0 else no_approved_list
        except rel_user_minutes_assistance.DoesNotExist:
            print "NO HAY rel_user_minutes_assistance NO_APPROVED_LIST"
        except Exception, e:
            print "Error NO_APPROVED_LIST:", e

        ######## </APPROVED LISTS> #########

        ######## <PREV and NEXT> #########
        prev, next = getPrevNextOfGroup(group, minutes_current)
        ######## </PREV and NEXT> #########
        ctx = {"group": group, "minutes": minutes_current, "prev": prev, "next": next,
        "m_assistance": m_assistance, "m_no_assistance": m_no_assistance, "pdf_address": pdf_address,
        "minute_template": loader.render_to_string(address_template, {"newMinutesForm": list_newMinutesForm}),
        "my_attending": my_attending,
        "missing_approved_list": missing_approved_list,
        "approved_list": approved_list, "no_approved_list": no_approved_list
        }
    else:
        return HttpResponseRedirect('/groups/#error-its-not-your-group')
    return render_to_response('groups/showMinutes.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def setApprove(request):
    if request.is_ajax():
        if request.method == 'GET':
            minutes_id = str(request.GET['m_id'])
            approved = 1 if int(request.GET['approve']) == 1 else 2
            print "m %s, a %s" % (minutes_id, approved)
            try:
                _minutes = minutes.objects.get(id=minutes_id)
                sign = rel_user_minutes_assistance(
                    id_minutes=_minutes,
                    id_user=request.user,
                    assistance=approved)
                sign.save()
                rol = rol_user_minutes.objects.get(id_minutes=_minutes, id_user=request.user)
                rol.is_active = True
                rol.save()
            except Exception, e:
                print "Error Al Firmar" % e
            response = {"approved": approved, "minutes": minutes_id, "user-id": request.user.id, "user-name": request.user.first_name + " " + request.user.last_name}
    else:
        response = "Error invitacion"
    return HttpResponse(json.dumps(response), mimetype="application/json")


def getMembersOfGroupWithSelected(group, select):
    '''
    return a tuple with the list of selected members and no selected members
    (selected_members, no_selected_members)
    the tuple is a rel_user_group object
    '''
    all_members = rel_user_group.objects.filter(id_group=group, is_active=True).order_by("id")
    memb_list = list()
    for m in all_members:
        memb_list.append(int(m.id_user.id))  # lista con id de todos los miembros del grupo
    # print memb_list
    selected_list = list()
    for l in select:
        selected_list.append(int(l))  # Lista de usuarios seleccionados
    # print selected_list
    no_selected_list = list(set(memb_list) - set(selected_list))  # lista de usuarios no seleccionados
    # print no_selected_list
    try:
        selected_members = rel_user_group.objects.filter(id_group=group, id_user__in=selected_list, is_active=True)
        no_selected_members = rel_user_group.objects.filter(id_group=group, id_user__in=no_selected_list, is_active=True)
    except rel_user_group.DoesNotExist:
        return None
    except Exception, e:
        raise e
        return None
    return (selected_members, no_selected_members)


def setMinuteAssistance(minutes_id, members_selected, members_no_selected):
    '''
    Stored in the database records all users attending a reunion.
    '''
    a = list()
    b = list()
    for m in members_selected:
        a.append(
            rel_user_minutes_assistance(
                id_user=m.id_user,
                id_minutes=minutes_id,
                assistance=True
                )
        )
    for m in members_no_selected:
        b.append(
            rel_user_minutes_assistance(
                id_user=m.id_user,
                id_minutes=minutes_id,
                assistance=False
                )
        )
    try:
        rel_user_minutes_assistance.objects.bulk_create(a)
        rel_user_minutes_assistance.objects.bulk_create(b)
    except Exception, e:
        print e
        return "Exception"


@login_required(login_url='/account/login')
def saveMinute(request, group, form, _template):
    '''
    Save the minutes in the tables of data base: minutes_type_1, minutes
    return:
    '''
    if getRelUserGroup(request.user, group).is_secretary:
        df = {
        'code': form.cleaned_data['code'],
        'date_start': form.cleaned_data['date_start'],
        'date_end': form.cleaned_data['date_end'],
        'location': form.cleaned_data['location'],
        'agenda': form.cleaned_data['agenda'],
        'agreement': form.cleaned_data['agreement'],
        'type_reunion': form.cleaned_data['type_reunion'],
        }
        try:
            minu = minutes.objects.get(id_group=group, code=df['code'])
        except minutes.DoesNotExist, e:
            print "Save minutes error:", e
            minu = None
        if not minu:
            myNewMinutes_type_1 = minutes_type_1(
                           date_start=df['date_start'],
                           date_end=df['date_end'],
                           location=df['location'],
                           agenda=df['agenda'],
                           agreement=df['agreement'],
                           type_reunion=df['type_reunion']
                         )
            myNewMinutes_type_1.save()
            myNewMinutes = minutes(
                            code=df['code'],
                            id_extra_minutes=myNewMinutes_type_1.pk,
                            id_group=group,
                            id_template=_template,
                        )
            myNewMinutes.save()
            id_user = request.user
            saveActionLog(id_user, 'NEW_MINUTE', "group: %s, code: %s" % (group.name, df['code']), request.META['REMOTE_ADDR'])
            # registra los usuarios que asistieron a la reunión en la que se creó el acta
            # setMinuteAssistance(myNewMinutes, m_selected, m_no_selected)
            return myNewMinutes
        else:
            return False
    else:
        return False


def getLastMinutes(group):
    try:
        l = minutes.objects.filter(id_group=group).order_by("-date_created")[0]
        return l
    except Exception, e:
        print e
        return "---"


def getEmailListByGroup(group):
    '''
    Retorna los correos de los miembros activos de un grupo.
    '''
    try:
        group_list = rel_user_group.objects.filter(id_group=group, is_active=True)
        mails = list()
        for member in group_list:
            mails.append(member.id_user.email)
        return mails
    except Exception, e:
        print e


@login_required(login_url='/account/login')
def rolesForMinutes(request, slug_group, id_reunion):
    '''
    return the board to give roles for a new minutes
    '''
    try:
        if id_reunion:
            reunion = reunions.objects.get(id=id_reunion).id
        else:
            reunion = ""
    except reunions.DoesNotExist:
        reunion = ""
    g = getGroupBySlug(slug_group)
    _user_rel = getRelUserGroup(request.user, g.id)
    if _user_rel.is_secretary and _user_rel.is_active:
        members = rel_user_group.objects.filter(id_group=g, is_member=True).order_by("-is_active")
        _members = list()
        for m in members:
            try:
                rel = rol_user_minutes.objects.get(id_group=g, id_user=m.id_user, id_minutes=None, is_active=False)
            except rol_user_minutes.DoesNotExist:
                rel = None
            _members.append({"member": m, "rol": rel})
            try:
                _secretary = rol_user_minutes.objects.get(id_group=g, is_active=False, is_secretary=True).id_user.id
            except rol_user_minutes.DoesNotExist:
                _secretary = None
            except Exception:
                _secretary = None
            try:
                _president = rol_user_minutes.objects.get(id_group=g, is_active=False, is_president=True).id_user.id
            except rol_user_minutes.DoesNotExist:
                _president = None
            except Exception:
                _president = None
        # members = rol_user_minutes.objects.filter(id_group=g, id_minutes=None, is_active=False)
        ctx = {"group": g, "is_admin": _user_rel.is_admin, "is_secretary": _user_rel.is_secretary, "members": _members, "id_reunion": reunion, "secretary": _secretary, "president": _president}
        return render_to_response('groups/rolesForMinutes.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/groups/' + str(g.slug) + "#necesitas-ser-redactor")


@login_required(login_url='/account/login')
def newMinutes(request, slug_group, id_reunion, slug_template):
    '''
    This function creates a minutes with the form for this.
    '''
    reunion = None
    hM = True
    group = getGroupBySlug(slug_group)
    print "slug_template: ", slug_template
    if slug_template:
        try:
            _template = templates.objects.get(slug=slug_template)
        except templates.DoesNotExist:
            raise Http404
    else:
        _template = templates.objects.get(slug='basica-1')

    list_templates = templates.objects.filter(is_public=True)
    list_private_templates = private_templates.objects.filter(id_group=group)
    _user_rel = getRelUserGroup(request.user, group.id)
    if _user_rel.is_secretary and _user_rel.is_active:
        if request.method == "POST":
            form = newMinutesForm(request.POST)
            select = request.POST.getlist('members[]')
            #  m_selected, m_no_selected = getMembersOfGroupWithSelected(group.id, select)
            m_assistance = None
            m_no_assistance = None
            if form.is_valid():
                try:
                    reunion_id = int(request.POST['reunion_id'])
                    _reunion = reunions.objects.get(id=reunion_id)
                    #  esta reunion pertenece a un grupo mio?
                    hM = _reunion.hasMinutes()
                    if hM:
                        return HttpResponseRedirect("/#ya-existe-un-acta-para-esta-reunion")
                except rel_reunion_minutes.DoesNotExist:
                    reunion_id = None
                except reunions.DoesNotExist:
                    reunion_id = None
                except Exception:
                    reunion_id = False
                _minute = saveMinute(request, group, form, _template)
                if _minute:
                    if not hM:
                        rel_reunion_minutes(id_reunion=_reunion, id_minutes=_minute).save()
                    try:
                        rols = rol_user_minutes.objects.filter(id_group=group, is_active=False)
                        for r in rols:
                            r.is_active = True
                            r.id_minutes = _minute
                            r.save()
                        email_list = list()
                        for rol in rols:
                            if rol.is_approver:
                                email_list.append(rol.id_user.email)
                                rel_user_minutes_assistance(id_user=rol.id_user, id_minutes=_minute, assistance=0).save()
                        # send email to the approvers
                    except Exception, e:
                        print "newMinutes Error", e
                    saved = True
                    error = False
                    url_new_minute = "/groups/" + str(group.slug) + "/minutes/" + str(_minute.code)
                    link = URL_BASE + url_new_minute
                    # email_list = getEmailListByGroup(group)
                    print "EMAILS", email_list
                    email_ctx = {
                                'firstname': request.user.first_name,
                                'username': request.user.username,
                                'groupname': group.name,
                                'link': link,
                                'urlgravatar': showgravatar(request.user.email, 50)
                                }
                    sendEmailHtml(3, email_ctx, email_list)
                    return HttpResponseRedirect(url_new_minute)
                else:
                    saved = False
                    error = "e2"  # error, mismo código de acta, o error al guardar en la db
            else:
                saved = False
                error = "e0"  # error, el formulario no es valido
                # if len(select) == 0:
                #     error = "e1"  # error, al menos un (1) miembro debe ser seleccionado
        else:
            saved = False
            error = False
            if id_reunion:
                try:
                    reunion = reunions.objects.get(id=id_reunion)
                    form = newMinutesForm(initial={"location": reunion.locale})
                except reunions.DoesNotExist:
                    reunion = None
                except Exception, e:
                    form = None
                    reunion = None
                    m_assistance = None
                    m_no_assistance = None
                    error = "e3"
                    print "Exception newReunion: %s" % e
            else:
                form = newMinutesForm()
                reunion = None
            try:
                m_assistance = rol_user_minutes.objects.filter(id_group=group.id, is_assistant=True, is_active=False)
                m_no_assistance = rol_user_minutes.objects.filter(id_group=group.id, is_assistant=False, is_active=False)
            except rel_user_group.DoesNotExist:
                m_assistance = None
                m_no_assistance = None
            except Exception, e:
                print "Exception members in newMinutes: %e" % e
        last = getLastMinutes(group)
        ctx = {'TITLE': "Nueva Acta",
               "newMinutesForm": form,
               "group": group,
               "reunion": reunion,
               "members_selected": m_assistance,
               "members_no_selected": m_no_assistance,
               "minutes_saved": {"saved": saved, "error": error},
               "last": last,
               "minutesTemplateForm": _template.address_template,
               "minutesTemplateJs": _template.address_js,
               "list_templates": list_templates,
               "list_private_templates": list_private_templates
               }
        return render_to_response('groups/newMinutes.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/groups/" + group.slug + "#No-tienes-permiso-para-crear-actas")


@login_required(login_url='/account/login')
def newReunion(request, slug):
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
                    email_list.append(str(relation.id_user.email) + ",")
                email_ctx = {'firstname': request.user.first_name,
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
                sendEmailHtml(2, email_ctx, email_list)
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
                         "date": (datetime.datetime.strftime(make_naive(reunion.date_reunion, get_default_timezone()), "%d de %B de %Y a las %I:%M %p")),
                         'is_confirmed': str(is_confirmed),
                         'is_saved': is_saved,
                         "title": reunion.title,
                         'is_last': is_last}
        i = i + 1
    response = json_array
    ctx = {'TITLE': "Actarium",
       "reunions_day": my_reu,
       "reunions": my_reu,
       "my_reu_day_json": json.dumps(response),
       "groups": gr}
    return render_to_response('groups/calendar.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def calendarDate(request, slug=None):
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
                         "date": (datetime.datetime.strftime(make_naive(reunion.date_reunion, get_default_timezone()), "%d de %B de %Y a las %I:%M %p")),
                         'is_confirmed': str(is_confirmed),
                         'is_saved': is_saved,
                         'title': reunion.title,
                         'is_last': is_last}
        i = i + 1
    response = json_array
    ctx = {'TITLE': "Actarium",
       "reunions_day": my_reu_day,
       "reunions": my_reu,
       "my_reu_day_json": json.dumps(response),
       "groups": gr}
    return render_to_response('groups/calendar.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def getReunions(request):
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
                                 "date": (datetime.datetime.strftime(make_naive(reunion.date_reunion, get_default_timezone()), "%d de %B de %Y a las %I:%M %p")),
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
                                         "date": (datetime.datetime.strftime(make_naive(reunion.date_reunion, get_default_timezone()), "%d de %B de %Y a las %I:%M %p")),
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
            email_list.append(str(id_reunion.id_convener.email) + ",")
            ctx_email = {
                 'firstname': request.user.first_name,
                 'username': request.user.username,
                 'response': resp,
                 'groupname': id_reunion.id_group.name,
                 'titlereunion':  id_reunion.title,
                 'urlgravatar': showgravatar(request.user.email, 50)
             }
            saveActionLog(id_user, 'SET_ASSIST', "id_reunion: %s, is_confirmed: %s" % (id_reunion.pk, is_confirmed), request.META['REMOTE_ADDR'])
            datos = "id_reunion = %s , id_user = %s , is_confirmed = %s, created %s" % (id_reunion.pk, id_user, is_confirmed, created)
            sendEmailHtml(5, ctx_email, email_list)
        return HttpResponse(json.dumps(datos), mimetype="application/json")
    else:
        response = "Error Calendar"
        return HttpResponse(json.dumps(response), mimetype="application/json")


@login_required(login_url='/account/login')
def getReunionData(request):
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
            reunion_data = {"convener": convener,
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

@login_required(login_url='/account/login')
def uploadMinutes(request, slug_group):
    group = groups.objects.get(slug=slug_group, is_active=True)
    is_member = rel_user_group.objects.filter(id_group=group.id, id_user=request.user)
    datos_validos = ""
    if is_member:
        if getRelUserGroup(request.user, group).is_secretary:
            if request.method == "POST":
                form = uploadMinutesForm(request.POST,request.FILES)
                if form.is_valid():
                    from groups.validators import validateExtension
                    for f in request.FILES.getlist('minutesFile'):
                        if validateExtension(f.name):
                            _last_minutes = last_minutes(
                                id_user = request.user,
                                address_file = f,
                                name_file = f.name
                            )
                            import random
                            _last_minutes.save()
                            _minutes = minutes(
                                id_group = group,
                                id_extra_minutes = _last_minutes.pk,
                                id_type = minutes_type.objects.get(pk=2),
                                is_valid = False,
                                is_full_signed = False,
                                code = "%s-%s"%(int(random.random()*1000000),_last_minutes.pk)
                            )
                            _minutes.save()
                        else:
                            print "invalid_extension in ", f.name
                else:
                    print "EL formulario no es valido"
            else:
                form = uploadMinutesForm()
                try:
                    datos_validos = request.GET['valid']
                except:
                    print ""
            last_minutes_list = []
            i = 0
            lml = minutes.objects.filter(id_group = group, id_type = minutes_type.objects.get(pk=2),is_valid = False)
            for m in lml:
                last_minutes_list.append({'i':i,'lm':last_minutes.objects.get(pk=m.id_extra_minutes).name_file,'lm_id':last_minutes.objects.get(pk=m.id_extra_minutes).pk})
                i = i+1
            _minutes = minutes.objects.filter(id_group = group, is_valid= True).order_by('-code')
            ctx={
                 'uploadMinutesForm':form, 
                 'group':group, 
                 'last_minutes':last_minutes_list, 
                 'datasize': len(last_minutes_list), 
                 'datos_validos':datos_validos, 
                 'minutes': _minutes}
            return render_to_response('groups/uploadMinutesForm.html', ctx, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect("/groups/" + group.slug + "?no_redactor=true") 
    else:
        return HttpResponseRedirect('/groups/#error-view-group')

@login_required(login_url='/account/login')
def uploadMinutesAjax(request):
    if request.is_ajax():
        if request.method == 'GET':
            last_minutes_get = request.GET['last_minutes']
            a = json.loads(last_minutes_get)
            group_id= a['group_id']
            group = groups.objects.get(pk=group_id)
            print "gurpo -------------------------------------------", group_id
            a = a['values']
            valid = True
            for m in a:
                if not(a[m]['code'] == "") and not(getMinutesByCode(group, a[m]['code'])):
                    print a[m]['name'],a[m]['code'],a[m]['lmid']
                    lm_temp = minutes.objects.get(id_extra_minutes = a[m]['lmid'], id_type = minutes_type.objects.get(pk=2))
                    lm_temp.code = a[m]['code']
                    lm_temp.is_valid = True
                    lm_temp.save()
                else:
                    valid = False
                print "existe el codigo?", getMinutesByCode(group, a[m]['code'])
            if valid:
                response = {'data':"validos"}
            else:
                response = {'data':"no_validos"}
        else:
            response = {'data':"No es GET"}
    else:
        response = {'data':"No es AJAX"}
    return HttpResponse(json.dumps(response), mimetype="application/json")
