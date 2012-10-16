# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
import hashlib, urllib  # para gravatar

from groups.models import groups


def home(request):
    if request.user.is_authenticated():
        #-----------------<GRAVATAR>-----------------
        size = 100
        email = request.user.email
        default = "http://cms.myspacecdn.com/cms/Music%20Vertical/Common/Images/default_small.jpg"
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d': default, 's': str(size)})
        #-----------------</GRAVATAR>-----------------

        #-----------------</GRUPOS>-----------------
        gr = groups.objects.filter(rel_user_group__id_user=request.user)
        #-----------------</GRUPOS>-----------------

        ctx = {'TITLE': "Actarium", 'gravatar_url': gravatar_url, "groups": gr}
    else:
        ctx = {'TITLE': "Actarium"}

    return render_to_response('website/index.html', ctx, context_instance=RequestContext(request))


def about(request):
    return render_to_response('website/about.html', {}, context_instance=RequestContext(request))
