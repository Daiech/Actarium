# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
import datetime
import re
from django.utils.timezone import get_default_timezone, make_naive
from groups.models import groups, invitations, reunions, assistance
from django.utils import simplejson as json
from website.models import feedBack


def home(request):
    if request.user.is_authenticated():

        #-----------------</GRUPOS>-----------------
        gr = groups.objects.filter(rel_user_group__id_user=request.user)
        #-----------------</GRUPOS>-----------------

        #-----------------<INVITACIONES>-----------------
        my_inv = invitations.objects.filter(email_invited=request.user.email, is_active=True)
        #-----------------</INVITACIONES>-----------------

        #-----------------<REUNIONES>-----------------
        my_reu = reunions.objects.filter(id_group__in=gr, is_done=False).order_by("-date_convened")
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
                json_array.append({"id_reunion": str(reunion.id), "group_name": reunion.id_group.name, "date": (datetime.datetime.strftime(make_naive(reunion.date_reunion, get_default_timezone()), "%d de %B de %Y a las %I:%M %p")), "title": reunion.title})
#            i = i + 1

        ctx = {'TITLE': "Actarium", "groups": gr, "invitations": my_inv, "reunions": json_array}
    else:
        ctx = {'TITLE': "Actarium by Daiech"}

    return render_to_response('website/index.html', ctx, context_instance=RequestContext(request))


def sendFeedBack(request):
    '''
    Formulario para feedback
    '''
    if request.is_ajax():
        if request.method == 'GET':
            print request.GET
            rate = request.GET['rate']
            comment = request.GET['comment']
            mail = request.GET['email']
            if(validateEmail(mail)):
                feed = feedBack(type_feed=rate, email=mail, comment=comment)
                feed.save()
                response = {"feed_id": feed.id}
            else:
                response = {"error": "Correo invalido"}
            return HttpResponse(json.dumps(response), mimetype="application/json")
    else:
        return HttpResponseRedirect("/")
    return True


def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email):
            return True
        else:
            return False
    else:
        return False


def about(request):
    return render_to_response('website/about.html', {}, context_instance=RequestContext(request))







