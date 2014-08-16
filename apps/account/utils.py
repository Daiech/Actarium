#encoding:utf-8
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from apps.account.models import activation_keys
from apps.emailmodule.views import sendEmailHtml
from .templatetags.gravatartag import showgravatar

def getNextUsername(username):
    """
    the entry username is already exists.
    then, search a new username.
    """
    num = username.split("_")[-1]
    if num.isdigit():
        num = int(num) + 1
        username = "_".join(username.split("_")[:-1]) + "_" + str(num)
    else:
        username = username + "_1"
    try:
        User.objects.get(username=username)
        return getNextUsername(username)
    except User.DoesNotExist:
        return username.replace(" ", "-")


def validateUsername(username):
    try:
        User.objects.get(username=username)
        return getNextUsername(username)
    except User.DoesNotExist:
        return username.replace(" ", "-")


def newInvitedUser(email_to_invite, _user_from, first_name=False, last_name=False):
    '''crea un nuevo usuario inactivo desde invitacion y lo retorna'''
    try:
        _user = User.objects.get(email=email_to_invite)
        return _user
    except User.DoesNotExist:
        _user = None
    _username = email_to_invite.split("@")[0]
    _username = validateUsername(_username)
    if not first_name:
        first_name = _username
    if not last_name:
        last_name = ""
    
    _user = User.objects.create(username=_username, first_name=first_name, last_name=last_name, email=email_to_invite, is_active=False)
    
    ak = activation_keys.objects.create_key_to_user(_user)
    if _user and ak:
        _user.set_password(ak.activation_key[:8])
        _user.save()
        # saveActionLog: new user invited by _user_from
        print reverse("confirm_account", args=(ak.activation_key, 1, ))
        ctx_email = {
            'username': _user_from.username,
            'activation_key': ak.activation_key,
            'inv_code': ak.activation_key[5:20], ## var to define a invitation. (only it is needed in the url to redirect)
            'newuser_username': _username,
            'pass': ak.activation_key[:8],
            'urlgravatar': showgravatar(_user_from.email, 50)
        }
        sendEmailHtml(7, ctx_email, [email_to_invite])
        return _user
    else:
        return None
