#encoding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse

from account.forms import RegisterForm, UserForm , NewDNI
from django.template import RequestContext  # para hacer funcionar {% csrf_token %}

#Django Auth
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_complete, password_reset_confirm
from actions_log.views import saveActionLog, saveViewsLog
from django.contrib.auth.models import User
from django.utils.hashcompat import sha_constructor
import random
from emailmodule.views import sendEmailHtml
from account.templatetags.gravatartag import showgravatar
from groups.models import DNI, DNI_type, DNI_permissions
from django.utils import simplejson as json


#------------------------------- <Normal User>---------------------------
def newUser(request):
    '''
    crea un nuevo usuario usando un formulario propio
    '''
    saveViewsLog(request, "account.views.newUser")
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/account/')
    if request.method == "POST":
        formulario = RegisterForm(request.POST)
        if formulario.is_valid():
            # formulario.save()
            # user_name = formulario['username'].data
            email_user = formulario.cleaned_data['email']
            name_newuser = formulario.cleaned_data['username']
            activation_key = getActivationKey(email_user)
            new_user = formulario.save()
            new_user.is_active = False
            new_user.username = new_user.username.replace(" ", "-")
            try:
                new_user.save()
                from models import activation_keys
                activation_keys(id_user=new_user, email=email_user, activation_key=activation_key).save()
                saveActionLog(new_user, "SIGN_IN", "username: %s, email: %s" % (name_newuser, formulario['email'].data), str(request.META['REMOTE_ADDR']))  # Registro en el Action log
                sendEmailHtml(1, {'username': name_newuser, 'activation_key': activation_key}, [str(email_user)])  # Envio de correo con clave de activacion
                return render_to_response('account/registered.html', {'email_address': email_user}, context_instance=RequestContext(request))
            except:
                return HttpResponseRedirect('/#Error-de-registro-de-usuario')
            # return userLogin(request, user_name, formulario['password1'].data)
    else:
        formulario = RegisterForm()
    from website.views import getGlobalVar
    ctx = {'formNewUser': formulario, 'url_terms': getGlobalVar("URL_TERMS"), 'url_privacy': getGlobalVar("URL_PRIVACY")}
    return render_to_response('account/newUser.html', ctx, context_instance=RequestContext(request))
#    return render_to_response('account/newUser.html',{}, context_instance = RequestContext(request))


def getActivationKey(email_user):
    return sha_constructor(sha_constructor(str(random.random())).hexdigest()[:5] + email_user).hexdigest()


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
        return username


def validateUsername(username):
    try:
        User.objects.get(username=username)
        return getNextUsername(username)
    except User.DoesNotExist:
        return username.replace(" ", "-")


def newInvitedUser(email_to_invite, _user_from, first_name=False, last_name=False):
    '''
    crea un nuevo usuario inactivo desde invitacion y lo retorna
    '''
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
    try:
        _user = User(username=_username, first_name=first_name, last_name=last_name, email=email_to_invite, is_active=False)
        activation_key = getActivationKey(email_to_invite)
        _user.set_password(activation_key[:8])
        _user.save()
    except Exception, e:
        print "Error newInvitedUser: %s" % e
        return False
    try:
        from models import activation_keys
        activation_keys(id_user=_user, email=email_to_invite, activation_key=activation_key).save()
    except Exception, e:
        print "Error in activation_keys:", e
        #ERROR log
    if _user:
        # saveAction Log: new user invited by _user_from
        print "localhost:8000/account/activate/", activation_key, "/invited1"
        id_inv = activation_key[5:20]
        ctx_email = {
            'username': _user_from.username,
            'activation_key': activation_key,
            'id_inv': id_inv,
            'newuser_username': _username,
            'pass': activation_key[:8],
            'urlgravatar': showgravatar(_user_from.email, 50)
        }
        sendEmailHtml(7, ctx_email, [email_to_invite])
        return _user


def log_in(request):
    '''
        Inicia session de un usuario que usa el formulario propio del sistema.
        Retorna y crea una sesion de usuario
    '''
    saveViewsLog(request, "account.views.log_in")
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/account/')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            return userLogin(request, request.POST['username'], request.POST['password'])
        else:
            formulario = AuthenticationForm(request.POST)
    else:
        formulario = AuthenticationForm()
    return render_to_response('account/login.html', {'formulario': formulario}, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def log_out(request):
    '''
        Finaliza una sesion activa
    '''
    saveViewsLog(request, "account.views.log_out")
    try:
        _user = request.user
        saveActionLog(_user,  "LOG_OUT", "username: %s" % (_user.username), request.META['REMOTE_ADDR'])  # Guarda la accion de cerrar sesion
        logout(request)
    except Exception, e:
        print e
    return HttpResponseRedirect('/')


def userLogin(request, user_name, password):
    '''
        Autentica a un usuario con los parametros recibidos
        actualmente solo se loguea con username, se espera autenticar con mail
    '''
    saveViewsLog(request, "account.views.userLogin")
    try:
        next = request.GET['next']
    except Exception:
        next = '/'

    acceso = authenticate(username=user_name, password=password)
    if acceso is not None:
        if acceso.is_active:
            login(request, acceso)
            try:
                user_id = User.objects.get(username=user_name)
            except:
                user_id = User.objects.get(email=user_name)
            saveActionLog(user_id, "LOG_IN", "username: %s" % (user_name), request.META['REMOTE_ADDR'])  # Guarda la accion de inicar sesion
            return HttpResponseRedirect(next)
        else:
            return render_to_response('account/noactivo.html', context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/account/login?next=' + next)


#------------------------------- </Normal User>---------------------------


#--------------------------------<Cuenta de Usuario>----------------------
@login_required(login_url='/account/login')
def personalData(request):
    '''
        Control para usuarios logueados.
        se consultan los datos y se los envia al template para imprimirlos
    '''
    saveViewsLog(request, "account.views.personalData")
    last_data = "last=> username: %s, name: %s, last_name: %s, email %s" % (request.user.username, request.user.first_name, request.user.last_name, request.user.email)
    if request.method == "POST":
        form = UserForm(request.POST, instance=request.user)

        if form.is_valid():
            _email = form.cleaned_data['email']
            print "Correo a cambiar", _email
            try:
                _user = User.objects.get(email=_email)
                if request.user == _user:
                    print "Si se puede cambiar el correo, el usuario que lo tiene es el mismo."
                    saveActionLog(request.user, "CHG_USDATA", last_data, request.META['REMOTE_ADDR'])  # Guarda datos de usuarios antes de modificarse
                    form.save()
                    update = True
                    error_email = None
                else:
                    print "El correo no se puede cambiar, otro usuario tiene el este correo ya asignado"
                    error_email = True
                    update = False
            except User.DoesNotExist:
                print "No existe un usuario con ese correo, el correo puede ser asignado"
                saveActionLog(request.user, "CHG_USDATA", last_data, request.META['REMOTE_ADDR'])  # Guarda datos de usuarios antes de modificarse
                form.save()
                update = True
                error_email = None
            except User.MultipleObjectsReturned:
                print "Multiples objetos retornados, error en la base de datos, se debe revizar"
                error_email = True
                update = False
            except:
                print "Error desconocido"
                error_email = True
                update = False
        else:
            update = False
            error_email = None
    else:
        form = UserForm(instance=request.user)
        update = False
        error_email = None
    print "update: ", update
    ctx = {"formUser": form, "dataUpdate": update, "passwordUpdate": False, "error_email": error_email}
    return render_to_response('account/personal_data.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/account/login')
def changePassword(request):
    '''
        Opcion para cambiar password
    '''
    saveViewsLog(request, "account.views.savePassword")
    passUpdate = False
    if request.method == "POST":
        passUpdate = False
        passForm = PasswordChangeForm(data=request.POST, user=request.user)
        if passForm.is_valid():
            passForm.save()
            saveActionLog(request.user, "CHG_PASS", "Password changed", request.META['REMOTE_ADDR'])  # Guarda datos de usuarios antes de modificarse
            passUpdate = True
    else:
        passForm = PasswordChangeForm(user=request.user)
        passUpdate = False
    ctx = {"passForm": passForm, "dataUpdate": False, "passwordUpdate": passUpdate, "error_email": False}
    return render_to_response('account/password.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/account/login')
def dni(request):
    saveViewsLog(request, "account.views.dni")
    
    if request.method == "POST":
        formDNI = NewDNI(request.POST)
        if formDNI.is_valid():
            dni = formDNI.cleaned_data['dni']
            dni_type = DNI_type.objects.get(pk=formDNI.cleaned_data['dni_type'])
            try:
                _DNI = DNI.objects.get(id_user=request.user)
                _DNI.dni_value = dni
                _DNI.dni_type = dni_type
            except:
                _DNI = DNI(dni_value=dni,
                           dni_type=dni_type,
                           id_user=request.user)
            _DNI.save()
            dataSaved = True
        else:
            dataSaved = False
    else:
        dataSaved = False
        try:
            _DNI = DNI.objects.get(id_user=request.user)
            formDNI = NewDNI(initial={"dni": _DNI.dni_value, "dni_type": _DNI.dni_type.pk})
        except:
            formDNI = NewDNI()

    _dni_permissions = DNI_permissions.objects.filter(id_user=request.user)
    if len(_dni_permissions) > 0:
        permissions = True
    else:
        permissions = False

    # print "hay permissions? ", permissions, len(_dni_permissions)
    ctx = {'formDNI': formDNI, 'dataSaved': dataSaved, 'dni_permissions': _dni_permissions, 'permissions': permissions}
    return render_to_response('account/dni.html', ctx, context_instance=RequestContext(request))


def setDNIPermissions(request):
    """
        Set permissions for DNI
    """
    saveViewsLog(request, "groups.views.setDNIPermissions")
    error = False
    saved = False
    if request.is_ajax():
        if request.method == 'GET':
            try:
                pk_dni = int(request.GET['pk_dni'])
                state = int(request.GET['status'])
                _dni_permissions = DNI_permissions.objects.get(pk=pk_dni)
                _dni_permissions.state = state
                try:
                    _dni = DNI.objects.get(id_user=_dni_permissions.id_user)
                    _dni_permissions.save()
                    # print "pk_dni: ",pk_dni," status: ",state
                    saved = True
                except DNI.DoesNotExist:
                    error = "Aun no se has guardado un DNI, debes agregar primero tu informaci&oacute;n del DNI en <a href='/account/dni'>configuraci&oacute;n de DNI</a>"
                    saved = False
                except:
                    error = "Ha ocurrido un error"
                    saved = False
            except DNI_permissions.DoesNotExist:
                error = "No hay permisos asignados"
                saved = False
            except Exception, e:
                print e
                error = "Por favor recarga la p&aacute;gina e intenta de nuevo."
            if error:
                return HttpResponse(json.dumps({"error": error, "saved": False}), mimetype="application/json")
            response = {"saved": saved, "error": error}
            return HttpResponse(json.dumps(response), mimetype="application/json")
        else:
            return "Ha ocurrido un error"
    return True
# --------------------------------</Cuenta de Usuario>----------------------

# --------------------------------<Recuperacion de contrasena>----------------------


def password_reset2(request):
        """
        django.contrib.auth.views.password_reset view (forgotten password)
        """
        saveViewsLog(request, "account.views.password_reset2")
        if not request.user.is_authenticated():
            print "entro a password_reset2"
            try:
                return password_reset(request, template_name='account/password_reset_form.html', email_template_name='account/password_reset_email.html', subject_template_name='account/password_reset_subject.txt', post_reset_redirect='/account/password/reset/done/')
            except Exception:
                return HttpResponseRedirect("/account/password/reset/done/")
        else:
            print "no entro a password_reset2"
            return HttpResponseRedirect("/account/")


def password_reset_done2(request):
        """
        django.contrib.auth.views.password_reset_done - after password reset view
        """
        saveViewsLog(request, "account.views.password_reset_done2")
        if not request.user.is_authenticated():
            return password_reset_done(request, template_name='account/password_reset_done.html')
        else:
            return HttpResponseRedirect("/account/")


def password_reset_confirm2(request, uidb36, token):
        """
        django.contrib.auth.views.password_reset_done - after password reset view
        """
        saveViewsLog(request, "account.views.password_reset_confirm2")
        if not request.user.is_authenticated():
                print "entro a password_reset_confirm2"
                return password_reset_confirm(request, uidb36, token, template_name='account/password_reset_confirm.html', post_reset_redirect='/account/password/done/')
        else:
                print "no entro a password_reset_confirm2"
                return HttpResponseRedirect("/account/")


def password_reset_complete2(request):
        """
        django.contrib.auth.views.password_reset_done - after password reset view
        """
        saveViewsLog(request, "account.views.password_reset_complete2")
        if not request.user.is_authenticated():
                print "entro a password_reset_complete2"
                return password_reset_complete(request, template_name='account/password_reset_complete.html')
        else:
                print "no entro a password_reset_complete2"
                return HttpResponseRedirect("/account/")

# --------------------------------</Recuperacion de contrasena>----------------------

# ---------------------------------<activacion de cuenta>----------------------------


def activationKeyIsValid(activation_key):
    from account.models import activation_keys
    try:
        return activation_keys.objects.get(activation_key=activation_key, is_expired=False)
    except activation_keys.DoesNotExist:
        return False
    except Exception:
        return False


def confirm_account(request, activation_key, is_invited=False):
    saveViewsLog(request, "account.views.confirm_account")
    ak = activationKeyIsValid(activation_key)
    if ak:
        from groups.models import rel_user_group
        try:
            rels = rel_user_group.objects.filter(id_user=ak.id_user, is_active=False)
        except rel_user_group.DoesNotExist:
            return False
        except Exception:
            return False
        update = False
        if request.method == "POST":
            form = UserForm(request.POST, instance=ak.id_user)
            if form.is_valid():
                form.save()
                update = True
                return HttpResponseRedirect("/account/activate/" + activation_key + "?is_invited=1")
            else:
                update = False
        else:
            form = UserForm(initial={
                "username": ak.id_user.username,
                "first_name": ak.id_user.first_name,
                "last_name": ak.id_user.last_name,
                "email": ak.id_user.email
            })
        ctx = {"invitations": rels, "invited": True, "form": form, "update": update}
        return render_to_response('account/confirm_account.html', ctx, context_instance=RequestContext(request))
    else:
        return render_to_response('account/invalid_link.html', {}, context_instance=RequestContext(request))


def activate_account(request, activation_key):
    saveViewsLog(request, "account.views.activate_account")
    if activate_account_now(request, activation_key):
        try:
            is_invited = request.GET['is_invited']
        except Exception:
            is_invited = False
        return render_to_response('account/account_actived.html', {"invited": is_invited}, context_instance=RequestContext(request))
    else:
        return render_to_response('account/invalid_link.html', {}, context_instance=RequestContext(request))


def activate_account_now(request, activation_key):
    saveViewsLog(request, "account.views.activate_account_now")
    from models import activation_keys
    try:
        activation_obj = activation_keys.objects.get(activation_key=activation_key)
        if not activation_obj.is_expired:
            user = User.objects.get(id=activation_obj.id_user.pk)
            user.is_active = True
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            activation_obj.is_expired = True
            activation_obj.save()
            return True
        else:
            return False
    except activation_keys.DoesNotExist:
        return False
    except Exception:
        return False
