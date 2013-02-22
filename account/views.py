#encoding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from account.forms import RegisterForm, UserForm
from django.template import RequestContext  # para hacer funcionar {% csrf_token %}

#Django Auth
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_complete, password_reset_confirm
from actions_log.views import saveActionLog
from django.contrib.auth.models import User
from django.utils.hashcompat import sha_constructor
from django.core.mail import EmailMessage
import random
from emailmodule.views import sendEmailHtml 


#------------------------------- <Normal User>---------------------------
def newUser(request):
    '''
    crea un nuevo usuario usando un formulario propio
    '''
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
            try:
                new_user.save()
                from models import activation_keys
                activation_keys(id_user=new_user, email=email_user, activation_key=activation_key).save()
                saveActionLog(new_user, "SIGN_IN", "username: %s, email: %s" % (name_newuser, formulario['email'].data), str(request.META['REMOTE_ADDR'])) #Registro en el Action log
                sendEmailHtml(1,{'username': name_newuser,'activation_key': activation_key},[str(email_user)]) # Envio de correo con clave de activacion
                return render_to_response('account/registered.html', {'email_address': email_user}, context_instance=RequestContext(request))
            except:
                return HttpResponseRedirect('/#Error-de-registro-de-usuario')
            # return userLogin(request, user_name, formulario['password1'].data)
    else:
        formulario = RegisterForm()
    ctx = {'formNewUser': formulario}
    return render_to_response('account/newUser.html', ctx, context_instance=RequestContext(request))
#    return render_to_response('account/newUser.html',{}, context_instance = RequestContext(request))


def getActivationKey(email_user):
    return sha_constructor(sha_constructor(str(random.random())).hexdigest()[:5] + email_user).hexdigest()


def newInvitedUser(email_to_invite, username_invited):
    '''
    crea un nuevo usuario inactivo desde invitacion
    '''
    try:
        _user = User.objects.get(email=email_to_invite)
        return _user
    except User.DoesNotExist:
        _user = None
    _username = email_to_invite.split("@")[0]
    try:
        _user = User.objects.get(username=_username)
        return _user
    except User.DoesNotExist:
        _user = None
    try:
        _user = User(username=_username, first_name=_username, email=email_to_invite, is_active=False)
        activation_key = getActivationKey(email_to_invite)
        _user.set_password(activation_key[:8])
        _user.save()
        from models import activation_keys
        activation_keys(id_user=_user, email=email_to_invite, activation_key=activation_key).save()
    except activation_keys.DoesNotExist:
        return False
    except Exception, e:
        print "Error: %s" % e
        return False
    try:
        id_inv = activation_key[5:20]
        title = username_invited + u" te invitó a Actarium, La plataforma de gestión de Actas y reuniones."
        contenido = "Bienvenido a Actarium!<br><br><strong>" + username_invited + "</strong> te invit&oacute; a registrarte en Actarium.<br><br><br>Debes ingresar al siguiente link para activar tu cuenta: <a href='http://actarium.daiech.com/account/activate/" + activation_key + "/invited" + id_inv + "' >http://actarium.daiech.com/account/activate/" + activation_key + "</a>, si no lo haces, no se activar&aacute; tu cuenta<br><br>Datos Temporales:<br><ul><li>Nombre de usuario: <strong>" + _username + "</strong></li><li>Contrase&ntilde;a: <strong>" + activation_key[:8] + "</strong></li></ul><br><br><br>Qu&eacute; es Actarium? <br>Actarium es la plataforma para la gesti&oacute;n de cualquier tipo de actas y reuniones.<br><br>Ent&eacute;rate de Actarium en <a href='http://actarium.com/about'>http://actarium.com/about</a>"
        print "localhost:8000/account/activate/" + activation_key + "/invited" + id_inv
        sendEmail([email_to_invite], title, contenido)
    except Exception, e:
        print "Exception mail: %s" % e

    return _user


def log_in(request):
    '''
        Inicia session de un usuario que usa el formulario propio del sistema.
        Retorna y crea una sesion de usuario
    '''
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
    saveActionLog(request.user,  "LOG_OUT", "username: %s" % (request.user), request.META['REMOTE_ADDR'])  # Guarda la accion de cerrar sesion
    logout(request)
    return HttpResponseRedirect('/')


def userLogin(request, user_name, password):
    '''
        Autentica a un usuario con los parametros recibidos
        actualmente solo se loguea con username, se espera autenticar con mail
    '''
    try:
        next = request.GET['next']
    except Exception:
        next = '/'
    acceso = authenticate(username=user_name, password=password)
    if acceso is not None:
        if acceso.is_active:
            login(request, acceso)
            user_id = User.objects.get(username=user_name)
            saveActionLog(user_id, "LOG_IN", "username: %s" % (user_name), request.META['REMOTE_ADDR'])  # Guarda la accion de inicar sesion
            return HttpResponseRedirect(next)
        else:
            return render_to_response('account/noactivo.html', context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/account/login?next=' + next)


#------------------------------- </Normal User>---------------------------


#--------------------------------<Cuenta de Usuario>----------------------
@login_required(login_url='/account/login')
def myAccount(request):
    '''
        Control para usuarios logueados.
        se consultan los datos y se los envia al template para imprimirlos
    '''
    last_data = "last=> username: %s, name: %s, last_name: %s, email %s" % (request.user.username, request.user.first_name, request.user.last_name, request.user.email)
    if request.method == "POST":
        form = UserForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            saveActionLog(request.user, "CHG_USDATA", last_data, request.META['REMOTE_ADDR'])  # Guarda datos de usuarios antes de modificarse
            update = True
        else:
            update = False
    else:
        form = UserForm(instance=request.user)
        update = False
    passForm = PasswordChangeForm(user=request.user)
    ctx = {"formUser": form, "passForm": passForm, "dataUpdate": update, "passwordUpdate": False}
    return render_to_response('account/index.html', ctx, context_instance=RequestContext(request))


def PasswordChange(request):
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
    form = UserForm(instance=request.user)
    ctx = {"formUser": form, "passForm": passForm, "dataUpdate": False, "passwordUpdate": passUpdate}
    return render_to_response('account/index.html', ctx, context_instance=RequestContext(request))

# --------------------------------</Cuenta de Usuario>----------------------

# --------------------------------<Recuperacion de contrasena>----------------------


def password_reset2(request):
        """
        django.contrib.auth.views.password_reset view (forgotten password)
        """
        if not request.user.is_authenticated():
            print "entro a password_reset2"
            return password_reset(request, template_name='account/password_reset_form.html', email_template_name='emailmodule/email_password_reset.html', subject_template_name='account/password_reset_subject.txt', post_reset_redirect='/account/password/reset/done/')
        else:
            print "no entro a password_reset2"
            return HttpResponseRedirect("/account/")


def password_reset_done2(request):
        """
        django.contrib.auth.views.password_reset_done - after password reset view
        """
        if not request.user.is_authenticated():
                print "entro a password_reset_done2"
                return password_reset_done(request, template_name='account/password_reset_done.html')
        else:
                print "no entro a password_reset_done2"
                return HttpResponseRedirect("/account/")


def password_reset_confirm2(request, uidb36, token):
        """
        django.contrib.auth.views.password_reset_done - after password reset view
        """
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
        if not request.user.is_authenticated():
                print "entro a password_reset_complete2"
                return password_reset_complete(request, template_name='account/password_reset_complete.html')
        else:
                print "no entro a password_reset_complete2"
                return HttpResponseRedirect("/account/")

# --------------------------------</Recuperacion de contrasena>----------------------

# ---------------------------------<activacion de cuenta>----------------------------


def activate_account(request, activation_key, is_invited=False):
    if not(activate_account_now(request, activation_key) == False):
        return render_to_response('account/account_actived.html', {"invited": is_invited}, context_instance=RequestContext(request))
    else:
        return render_to_response('account/invalid_link.html', {}, context_instance=RequestContext(request))


def activate_account_now(request, activation_key):
    from models import activation_keys
    try:
        activation_obj = activation_keys.objects.get(activation_key=activation_key)
    except Exception:
        return False
    if not(activation_obj.is_expired):
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


def sendEmail(mail_to, titulo, contenido):
    contenido = contenido + "\n" + "<br><br><p style='color:gray'>Mensaje enviado autom&aacute;ticamente por <a style='color:gray' href='http://daiech.com'>Daiech</a>. <br><br> Escribenos en twitter<br> <a href='http://twitter.com/Actarium'>@Actarium</a> - <a href='http://twitter.com/Daiech'>@Daiech</a></p><br><br>"
    try:
        correo = EmailMessage(titulo, contenido, 'Actarium <no-reply@daiech.com>', mail_to)
        correo.content_subtype = "html"
        correo.send()
    except Exception, e:
        print e
