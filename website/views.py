# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
import hashlib,urllib #para gravatar


#-- TOCA CALCULAR LA IMAGEN DE GRAVATAR UNA SOLA VEZ Y AGRAGARLA A LA SESION DE USUARIO
#--

def home(request):
    if request.user.is_authenticated():
        size = 100
        email = request.user.email
        default = "http://cms.myspacecdn.com/cms/Music%20Vertical/Common/Images/default_small.jpg"
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
        ctx = {'TITLE':"Actarium",
               'gravatar_url': gravatar_url}
    else:
        ctx = {'TITLE':"Actarium"}
    return render_to_response('website/index.html', ctx, context_instance = RequestContext(request))


def about(request):
    return render_to_response('website/index.html', {}, context_instance = RequestContext(request))
