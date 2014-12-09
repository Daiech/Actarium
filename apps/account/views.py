#encoding:utf-8
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext  # para hacer funcionar {% csrf_token %}
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_complete, password_reset_confirm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .forms import RegisterForm, UserForm , NewDNI
from apps.emailmodule.views import sendEmailHtml
from apps.actions_log.views import saveActionLog, saveViewsLog
from apps.groups_app.models import DNI, DNI_type, DNI_permissions
from actarium_apps.organizations.models import rel_user_group
from .models import activation_keys
from hashlib import sha256 as sha_constructor
import json

#------------------------------- <Normal User>---------------------------
@login_required(login_url='/account/login')
def complete_registration(request):
    if request.method == "POST":
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("tour"))
    else:
        form = UserForm(instance=request.user)
    return render(request, "account/complete_registration.html", locals())


def newUser(request):
    '''
    crea un nuevo usuario usando un formulario propio
    '''
    saveViewsLog(request, "apps.account.views.newUser")
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/account/')
    if request.method == "POST":
        formulario = RegisterForm(request.POST)
        if formulario.is_valid():
            email_user = formulario.cleaned_data['email']
            name_newuser = formulario.cleaned_data['username']
            new_user = formulario.save()
            new_user.is_active = False
            new_user.username = new_user.username.replace(" ", "-")
            try:
                new_user.save()
                ak = activation_keys.objects.create_key_to_user(new_user)
                saveActionLog(new_user, "NEW_USER_CREATED", "username: %s, email: %s" % (name_newuser, formulario['email'].data), str(request.META['REMOTE_ADDR']))  # Registro en el Action log
                sendEmailHtml(1, {'username': name_newuser, 'activation_key': ak.activation_key}, [str(email_user)])  # Envio de correo con clave de activacion
                return render_to_response('account/registered.html', {'email_address': email_user}, context_instance=RequestContext(request))
            except:
                return HttpResponseRedirect('/#Error-de-registro-de-usuario')
            # return userLogin(request, user_name, formulario['password1'].data)
    else:
        formulario = RegisterForm()
    from apps.website.views import getGlobalVar
    ctx = {'formulario': formulario, 'url_terms': getGlobalVar("URL_TERMS"), 'url_privacy': getGlobalVar("URL_PRIVACY")}
    return render_to_response('account/newUser.html', ctx, context_instance=RequestContext(request))
#    return render_to_response('account/newUser.html',{}, context_instance = RequestContext(request))


def log_in(request):
    '''
        Inicia session de un usuario que usa el formulario propio del sistema.
        Retorna y crea una sesion de usuario
    '''
    saveViewsLog(request, "apps.account.views.log_in")
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/account')
    if request.method == 'POST':
        formulario = AuthenticationForm(data=request.POST)
        if formulario.is_valid():
            return userLogin(request, request.POST.get('username'), request.POST.get('password'))
    else:
        next = request.GET.get('next') if 'next' in request.GET else ""
        formulario = AuthenticationForm()
    return render(request, 'account/login.html', locals())


@login_required(login_url='/account/login')
def log_out(request):
    '''
        Finaliza una sesion activa
    '''
    saveViewsLog(request, "apps.account.views.log_out")
    try:
        _user = request.user
        saveActionLog(_user,  "LOG_OUT", "username: %s" % (_user.username), request.META['REMOTE_ADDR'])  # Guarda la accion de cerrar sesion
        logout(request)
    except Exception, e:
        print e
    return HttpResponseRedirect('/')


def userLogin(request, user_name, password):
    '''Autentica a un usuario con los parametros recibidos
        actualmente solo se loguea con username, se espera autenticar con mail'''
    saveViewsLog(request, "apps.account.views.userLogin")
    next = request.GET.get('next') if 'next' in request.GET else None
    if not next:
        next = request.POST.get('next') if 'next' in request.POST else '/'
    user = authenticate(username=user_name, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            saveActionLog(user, "LOG_IN", "username: %s" % (user_name), request.META['REMOTE_ADDR'])  # Guarda la accion de inicar sesion
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
    saveViewsLog(request, "apps.account.views.personalData")
    last_data = "last=> username: %s, name: %s, last_name: %s, email %s" % (request.user.username, request.user.first_name, request.user.last_name, request.user.email)
    if request.method == "POST":
        form = UserForm(request.POST, instance=request.user)

        if form.is_valid():
            _email = form.cleaned_data['email']
            try:
                _user = User.objects.get(email=_email)
                if request.user == _user:
                    saveActionLog(request.user, "CHG_USDATA", last_data, request.META['REMOTE_ADDR'])  # Guarda datos de usuarios antes de modificarse
                    form.save()
                    update = True
                    error_email = None
                else:
                    error_email = True
                    update = False
            except User.DoesNotExist:
                saveActionLog(request.user, "CHG_USDATA", last_data, request.META['REMOTE_ADDR'])  # Guarda datos de usuarios antes de modificarse
                form.save()
                update = True
                error_email = None
            except User.MultipleObjectsReturned:
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
    saveViewsLog(request, "apps.account.views.savePassword")
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
    saveViewsLog(request, "apps.account.views.dni")
    
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

@login_required(login_url='/account/login')
def list_notifications(request):
    from apps.actions_log.models import UserNotification
    notifications = UserNotification.objects.filter(user=request.user).order_by('-created')
    return render(request,'notifications/notifications.html',locals())



def setDNIPermissions(request):
    """
        Set permissions for DNI
    """
    saveViewsLog(request, "apps.groups_app.views.setDNIPermissions")
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
    """django.contrib.auth.views.password_reset view (forgotten password)"""
    saveViewsLog(request, "apps.account.views.password_reset2")
    if not request.user.is_authenticated():
        try:
            return password_reset(request, template_name='account/password_reset_form.html', email_template_name='account/password_reset_email.html', subject_template_name='account/password_reset_subject.txt', post_reset_redirect='/account/password/reset/done/')
        except Exception:
            return HttpResponseRedirect("/account/password/reset/done/")
    else:
        return HttpResponseRedirect("/account/")


def password_reset_done2(request):
        """
        django.contrib.auth.views.password_reset_done - after password reset view
        """
        saveViewsLog(request, "apps.account.views.password_reset_done2")
        if not request.user.is_authenticated():
            return password_reset_done(request, template_name='account/password_reset_done.html')
        else:
            return HttpResponseRedirect("/account/")


def password_reset_confirm2(request, uidb36, token):
        """
        django.contrib.auth.views.password_reset_done - after password reset view
        """
        saveViewsLog(request, "apps.account.views.password_reset_confirm2")
        if not request.user.is_authenticated():
            return password_reset_confirm(request, uidb36, token, template_name='account/password_reset_confirm.html', post_reset_redirect='/account/password/done/')
        else:
            return HttpResponseRedirect("/account/")


def password_reset_complete2(request):
        """
        django.contrib.auth.views.password_reset_done - after password reset view
        """
        saveViewsLog(request, "apps.account.views.password_reset_complete2")
        if not request.user.is_authenticated():
                print "entro a password_reset_complete2"
                return password_reset_complete(request, template_name='account/password_reset_complete.html')
        else:
                print "no entro a password_reset_complete2"
                return HttpResponseRedirect("/account/")

# --------------------------------</Recuperacion de contrasena>----------------------

# ---------------------------------<activacion de cuenta>----------------------------


def activationKeyIsValid(activation_key):
    from apps.account.models import activation_keys
    try:
        return activation_keys.objects.get(activation_key=activation_key, is_expired=False)
    except activation_keys.DoesNotExist:
        return False
    except Exception:
        return False


def confirm_account(request, activation_key, is_invited=False):
    saveViewsLog(request, "apps.account.views.confirm_account")
    ak = activationKeyIsValid(activation_key)
    if ak:
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
    saveViewsLog(request, "apps.account.views.activate_account")
    if activate_account_now(request, activation_key):
        try:
            is_invited = request.GET['is_invited']
        except Exception:
            is_invited = False
        return render_to_response('account/account_actived.html', {"invited": is_invited}, context_instance=RequestContext(request))
    else:
        return render_to_response('account/invalid_link.html', {}, context_instance=RequestContext(request))


def activate_account_now(request, activation_key):
    saveViewsLog(request, "apps.account.views.activate_account_now")
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


@login_required()
def delete_account(request):
    print "hola, %s esta es la eliminacion" % request.user.username
    if request.method == "POST":
        request.user.delete()
        return HttpResponseRedirect(reverse("confirm_account_deleted"))
    return render(request, "account/delete_account.html", locals())


def confirm_account_deleted(request):
    return render(request, "account/confirm_account_deleted.html", locals())



