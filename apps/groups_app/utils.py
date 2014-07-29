#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.conf import settings

from actarium_apps.organizations.models import Organizations, Groups, rel_user_group
from .validators import validateEmail
from apps.account.templatetags.gravatartag import showgravatar
from apps.account.views import newInvitedUser
from apps.emailmodule.views import sendEmailHtml


def getUserByEmail(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None

def isMemberOfOrg(user, org):
    if user.organizationsuser_user.filter(organization=org, role__code="is_member").count() > 0:
        return True
    else:
        return False

def has_org_quota_for_user(org):
    """Consultar con los servicios activos de la organización"""
    return org.organizationservices_organization.can_add()


def sendInvitationToGroup(user_invited, user_from, group):
    '''Enviar una invitacion de grupo a un usuario'''
    try:
        _inv = setRelUserGroup(id_user=user_invited, id_user_invited=user_from, id_group=group, is_member=True, is_active=True)
        if _inv:
            group.organization.set_role(user_invited, is_member=True)
    except Exception, e:
        print "EROROR views.sendInvitationToGroup", e
        return False
    if _inv:
        email = [user_invited.email]
        ctx_email = {
            'firstname': user_from.first_name + user_from.last_name,
            'username': user_from.username,
            'groupname': group.name,
            'urlgravatar': showgravatar(user_from.email, 50)
        }
        sendEmailHtml(6, ctx_email, email, group)
    return _inv


def newUserWithInvitation(email, user_from, group, first_name=False, last_name=False):
    '''Crear un nuevo usuario.'''
    if validateEmail(email):
        try:
            if not getUserByEmail(email):
                _user = newInvitedUser(email, user_from, first_name=first_name, last_name=last_name)
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


def setRelUserGroup(id_user, id_group,
    id_user_invited=None,
    is_superadmin=False,
    is_admin=False,
    is_secretary=False,
    is_member=True,
    is_active=False):
    try:
        rel = rel_user_group(
            id_user=id_user,
            id_user_invited=id_user_invited,
            id_group=id_group,
            is_member=bool(is_member),
            is_admin=is_admin,
            is_secretary=is_secretary,
            is_superadmin=is_superadmin,
            is_active=is_active)
        rel.save()

        # saveAction new Rel user group
        return True
    except Exception, e:
        # error log
        print "EROROR en setRelUserGroup", e
        return False


def getRelUserGroup(_user, _group):
    try:
        return rel_user_group.objects.get(id_user=_user, id_group=_group)
    except rel_user_group.DoesNotExist:
        return False
    except Exception:
        return False


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
        setRelUserGroup(id_user=_user, id_group=_group, is_member=bool(is_member), is_active=is_active, is_admin=is_admin, is_secretary=is_secretary, is_superadmin=is_superadmin)


@login_required(login_url='/account/login')
def newBasicGroup(request, form, org):
    df = {
        'name': form.cleaned_data['name'],
        'description': form.cleaned_data['description'],
        'id_creator': request.user,
        # 'id_group_type': form.cleaned_data['id_group_type']  # Se omite para no pedir tipo de grupo
        'id_group_type': 1
    }
    myNewGroup = Groups(
        name=df['name'],
        description=df['description'],
        organization=org,
    )
    myNewGroup.save()
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
            setUserRoles(request.user, myNewGroup, is_member=1, is_active=True, is_secretary=1)
        if user_or_email['user'] != request.user:
            if user_or_email['user']:
                inv = sendInvitationToGroup(user_or_email['user'], request.user, myNewGroup)
                if inv:  # new rel to: Create group. Other is admin (other) # this is the group than only i administer
                    setUserRoles(user_or_email['user'], myNewGroup, is_superadmin=1, is_admin=1, is_active=False, is_secretary=1)
            else:
                _user = newUserWithInvitation(user_or_email['email'], request.user, myNewGroup)
                if _user:  # new rel to: Create group. Other is admin (other)
                    setUserRoles(_user, myNewGroup, is_superadmin=1, is_admin=1, is_active=False, is_secretary=1)

        else:  # new rel to: Create group. I'm admin
            setUserRoles(user_or_email['user'], myNewGroup, is_superadmin=1, is_admin=1, is_member=is_memb, is_active=1, is_secretary=1)
            print getRelUserGroup(user_or_email['user'], myNewGroup).is_admin
    else:
        print "No hay un administrador para este grupo"  # error! se dio atras al crear new group y no se selecciono un admin
    return myNewGroup


@login_required(login_url='/account/login')
def create_group(request, form):
    org_id = request.POST.get('sel-organization')
    # org = Organizations.objects.get_my_org_by_id(id=org_id, admin=request.user)
    org = request.user.organizationsuser_user.get_org(id=org_id)
    if org:
        new_group = newBasicGroup(request, form, org)
        return new_group
    else:
        return False


def getEmailListByGroup(group):
    '''Retorna los correos de los miembros activos de un grupo.'''
    try:
        group_list = rel_user_group.objects.filter(id_group=group, is_active=True)
        mails = []
        for member in group_list:
            mails.append(member.id_user.email)
        return mails
    except Exception, e:
        print e






def send_email_full_signed(minutes):
    try:
        link = settings.URL_BASE + reverse("show_minute", args=(minutes.id_group.slug, minutes.code, ))
        email_ctx = {
            'groupname': minutes.id_group.name,
            'code': minutes.code,
            'link': link
        }
        sendEmailHtml(3, email_ctx, getEmailListByGroup(minutes.id_group), minutes.id_group)
    except Exception, e:
        pass
