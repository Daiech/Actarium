# Create your views here.
#encoding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
import re
from groups.models import reunions, assistance, rel_user_group
from actions_log.views import saveActionLog, saveViewsLog
from groups.views import dateTimeFormatForm
from django.utils import simplejson as json
from website.models import *


def home(request):
    if request.user.is_authenticated():
        saveViewsLog(request,"Home_authenticated")
        #-----------------</GRUPOS>-----------------
        gr = rel_user_group.objects.filter(
            id_user=request.user,
            is_active=True,
            is_member=True
        )
        _groups_list = list()
        for g in gr:
            _groups_list.append(g.id_group.id)
        #-----------------</GRUPOS>-----------------

        #-----------------<INVITACIONES>-----------------
        my_inv = rel_user_group.objects.filter(id_user=request.user, is_active=False, is_member=True)
        #-----------------</INVITACIONES>-----------------

        #-----------------<REUNIONES>-----------------
        # my_reu = reunions.objects.filter(id_group__in=gr, is_done=False).order_by("-date_convened")
        my_reu = reunions.objects.filter(id_group__in=_groups_list).order_by("-date_convened")
        json_array = list()
        for reunion in my_reu:
            try:
                assistance.objects.get(id_user=request.user, id_reunion=reunion.pk)
            except assistance.DoesNotExist:
                json_array.append({
                    "id_reunion": str(reunion.id),
                    "group_name": reunion.id_group.name,
                    "date": dateTimeFormatForm(reunion.date_reunion),
                    "title": reunion.title})
        #-----------------</REUNIONES>-----------------

        ctx = {'my_reu': my_reu, "groups": gr, "invitations": my_inv, "reunions": json_array}
        template = 'website/index.html'
    else:
        saveViewsLog(request,"Home_anonymous")
        ctx = {}
        template = 'website/landing.html'

    return render_to_response(template, ctx, context_instance=RequestContext(request))


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


def help(request):
    try:
        faqs = faq.objects.filter(is_active=True)
    except faq.DoesNotExist:
        faqs = None
    return render_to_response('website/help.html', {"faqs": faqs}, context_instance=RequestContext(request))


def privacy_(request):
    try:
        p = privacy.objects.get(is_active=True)
    except privacy.DoesNotExist:
        p = None
    title = u"Políticas de privacidad"
    ctx = {"title": title, "content": p, "privacy": True, "terms": False}
    return render_to_response('website/conditions_privacy.html', ctx, context_instance=RequestContext(request))


def terms(request):
    try:
        t = conditions.objects.get(is_active=True)
    except conditions.DoesNotExist:
        t = None
    title = u"Términos y condiciones"
    ctx = {"title": title, "content": t, "privacy": False, "terms": True}
    return render_to_response('website/conditions_privacy.html', ctx, context_instance=RequestContext(request))


def getGlobalVar(name):
    try:
        return globalVars.objects.get(name=name).url
    except globalVars.DoesNotExist:
        return ""
    except Exception:
        return ""
