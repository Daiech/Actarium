from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from account.forms import RegisterForm, UserForm
from django.template import RequestContext  # para hacer funcionar {% csrf_token %}

#Django Auth
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm  # , PasswordResetForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset


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
            formulario.save()
            return userLogin(request, formulario['username'].data, formulario['password1'].data)
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
    logout(request)
    return HttpResponseRedirect('/')


def userLogin(request, user_name, password):
    '''
        Autentica a un usuario con los parametros recibidos
        actualmente solo se loguea con username, se espera autenticar con mail
    '''
    acceso = authenticate(username=user_name, password=password)
    if acceso is not None:
        if acceso.is_active:
            login(request, acceso)
            return HttpResponseRedirect('/#login')
        else:
            return render_to_response('account/status.html', context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/account/login#errorlogin')


#------------------------------- </Normal User>---------------------------


#--------------------------------<Cuenta de Usuario>----------------------
@login_required(login_url='/account/login')
def myAccount(request):
    '''
        Control para usuarios logueados.
        se consultan los datos y se los envia al template para imprimirlos
    '''
    if request.method == "POST":
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            update = True
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
            passUpdate = True
    else:
        passForm = PasswordChangeForm(user=request.user)
        passUpdate = False
    form = UserForm(instance=request.user)
    ctx = {"formUser": form, "passForm": passForm, "dataUpdate": False, "passwordUpdate": passUpdate}
    return render_to_response('account/index.html', ctx, context_instance=RequestContext(request))

# --------------------------------</Cuenta de Usuario>----------------------
