# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext

from groups.models import groups, invitations, reunions


def home(request):
    if request.user.is_authenticated():

        #-----------------</GRUPOS>-----------------
        gr = groups.objects.filter(rel_user_group__id_user=request.user)
        #-----------------</GRUPOS>-----------------

        #-----------------<INVITACIONES>-----------------
        my_inv = invitations.objects.filter(email_invited=request.user.email, is_active=True)
        #-----------------</INVITACIONES>-----------------

        #-----------------<REUNIONES>-----------------
        my_reu = reunions.objects.filter(id_group__in=gr, is_done=False)
        #-----------------</REUNIONES>-----------------

        ctx = {'TITLE': "Actarium", "groups": gr, "invitations": my_inv, "reunions": my_reu}
    else:
        ctx = {'TITLE': "Actarium"}

    return render_to_response('website/index.html', ctx, context_instance=RequestContext(request))


def about(request):
    return render_to_response('website/about.html', {}, context_instance=RequestContext(request))
