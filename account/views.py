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
import random

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
            email_list = []
            email_user = formulario.cleaned_data['email']
            name_newuser = formulario.cleaned_data['username']
            salt = sha_constructor(str(random.random())).hexdigest()[:5]
            activation_key = sha_constructor(salt+email_user).hexdigest()            
            new_user = formulario.save()
            new_user.is_active = False
            new_user.save()
            from models import activation_keys
            activation_keys(id_user=new_user, email=email_user, activation_key= activation_key).save()
            
            email_list.append(str(email_user) + ",")
            try:
                title = "Bienvenido a Actarium"
                contenido = "<strong>"+str(name_newuser)+"</strong> <br ><br> Te damos la bienvenida a Actarium, solo falta un paso para activar tu cuenta. <br > Ingresa al siguiente link para activar tu cuenta: <a href='http://actarium.daiech.com/account/activate/"+activation_key+"' >http://actarium.daiech.com/account/activate/"+activation_key+"</a>"
#                print contenido
                sendEmail(email_list, title, contenido)
            except Exception, e:
                print "Exception mail: %s" % e
            return render_to_response('account/registered.html')


            user_id = User.objects.get(username=name_newuser)
            saveActionLog(user_id, "SIGN_IN", "username: %s, email: %s" % (name_newuser, formulario['email'].data), str(request.META['REMOTE_ADDR']))
            # return userLogin(request, user_name, formulario['password1'].data)
    else:
        formulario = RegisterForm()
    ctx = {'formNewUser': formulario}
    return render_to_response('account/newUser.html', ctx, context_instance=RequestContext(request))
#    return render_to_response('account/newUser.html',{}, context_instance = RequestContext(request))


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
            return password_reset(request, template_name='account/password_reset_form.html', email_template_name='account/password_reset_email.html', subject_template_name='account/password_reset_subject.txt', post_reset_redirect='/account/password/reset/done/')
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

def activate_account(request,activation_key):
    if  not(activate_account_now(request,activation_key)== False):
        return render_to_response('account/account_actived.html',{},context_instance = RequestContext(request))
    else:
        return render_to_response('account/invalid_link.html')
    
    
def activate_account_now(request, activation_key):
    from models import activation_keys
    from django.contrib.auth.models import User
    try:
        activation_obj = activation_keys.objects.get(activation_key = activation_key)
    except  Exception, e:
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


