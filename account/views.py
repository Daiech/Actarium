from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from Actarium import settings
from account.forms import RegisterForm
from django.template import RequestContext #para hacer funcionar {% csrf_token %}

#Django Auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

# import code for encoding urls and generating md5 hashes --  GRAVATAR
import urllib, hashlib

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
            return userLogin(request,formulario['username'].data,formulario['password1'].data)
            
    else:
        formulario = RegisterForm()
    ctx = {'formNewUser': formulario}
    return render_to_response('account/newUser.html',ctx, context_instance=RequestContext(request))
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
            return userLogin(request,request.POST['username'],request.POST['password'])
        else:
            formulario = AuthenticationForm(request.POST)
    else:
        formulario = AuthenticationForm()   
    return render_to_response('account/login.html',{'formulario':formulario}, context_instance = RequestContext(request))

@login_required(login_url='/account/login')
def log_out(request):
    '''
        Finaliza una sesion activa
    '''
    logout(request)
    return HttpResponseRedirect('/')

def userLogin(request,user_name,password):
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
            return render_to_response('account/status.html', context_instance = RequestContext(request))
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
    usuario = request.user
    if request.user.is_authenticated():
        #-----------------<GRAVATAR>-----------------
        size = 100
        email = request.user.email
        default = "http://cms.myspacecdn.com/cms/Music%20Vertical/Common/Images/default_small.jpg"
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
        #-----------------</GRAVATAR>-----------------
    else:
        gravatar_url = "/static/website/img/user_default.png"
    ctx = {'user':usuario, 'gravatar_url': gravatar_url}
    return render_to_response('account/index.html',ctx, context_instance = RequestContext(request))

# --------------------------------</Cuenta de Usuario>----------------------




