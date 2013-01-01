# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime
from django.utils.timezone import make_aware, get_default_timezone, make_naive
from groups.models import groups, invitations, reunions, assistance


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
#        i = 0
        json_array = []
        for reunion in my_reu:
            try:
                confirm = assistance.objects.get(id_user=request.user, id_reunion=reunion.pk)
#                is_confirmed = confirm.is_confirmed
#                is_saved = 1
            except assistance.DoesNotExist:
#                is_confirmed = False
#                is_saved = 0
                json_array.append({"id_reunion": str(reunion.id), "group_name": reunion.id_group.name, "date": (datetime.datetime.strftime(make_naive(reunion.date_reunion, get_default_timezone()), "%I:%M %p"))})
#            i = i + 1

        ctx = {'TITLE': "Actarium", "groups": gr, "invitations": my_inv, "reunions": json_array}
    else:
        ctx = {'TITLE': "Actarium by Daiech"}

    return render_to_response('website/index.html', ctx, context_instance=RequestContext(request))


def about(request):
    return render_to_response('website/about.html', {}, context_instance=RequestContext(request))
