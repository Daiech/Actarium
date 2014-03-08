# Create your views here.
# encoding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson as json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import translation
from apps.groups_app.models import reunions, assistance, rel_user_group, DNI_permissions
from apps.groups_app.views import dateTimeFormatForm
from apps.actions_log.views import saveActionLog, saveViewsLog
from apps.emailmodule.views import sendEmailHtml
from apps.account.templatetags.gravatartag import showgravatar
from .models import *
from .utils import *
import datetime
import re


def home(request):
    if request.user.is_authenticated():
        saveViewsLog(request, "Home_authenticated")
        return organizations_index(request)
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
        my_inv = rel_user_group.objects.filter(
            id_user=request.user, is_active=False, is_member=True)
        #-----------------</INVITACIONES>-----------------

        _dni_permissions = DNI_permissions.objects.filter(
            id_user=request.user, state=0)

        #-----------------<REUNIONES>-----------------
        # my_reu = reunions.objects.filter(id_group__in=gr,
        # is_done=False).order_by("-date_convened")
        my_reu = reunions.objects.filter(
            id_group__in=_groups_list, date_reunion__gt=datetime.date.today()).order_by("-date_convened")
        json_array = list()
        for reunion in my_reu:
            try:
                assistance.objects.get(
                    id_user=request.user, id_reunion=reunion.pk)
            except assistance.DoesNotExist:
                json_array.append({
                    "id_reunion": str(reunion.id),
                    "id_group": reunion.id_group,
                    "date": dateTimeFormatForm(reunion.date_reunion),
                    "title": reunion.title})
        #-----------------</REUNIONES>-----------------

        ctx = {
            'my_reu': my_reu, "groups": gr, "invitations": my_inv, "reunions": json_array,
            'dni_permissions': _dni_permissions}
        template = 'website/index.html'
    else:
        saveViewsLog(request, "Home_anonymous")
        ctx = {}
        template = 'website/landing.html'
    # if request.method == "GET" and 'lang' in request.GET:
    #     try:
    #         lang_available = False
    #         for l in settings.LANGUAGES:
    #             if request.GET.get("lang") in l:
    #                 lang_available = True
    #         if lang_available:
    #             request.session['django_language'] = request.GET.get("lang")
    #             translation.activate(request.GET.get("lang"))
    #         else:
    #             ctx["no_supported"] = True
    #     except Exception, e:
    #         print e
    print "templateeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee:", template
    return render_to_response(template, ctx, context_instance=RequestContext(request))


def sendFeedBack(request):
    '''
    Formulario para feedback
    '''
    saveViewsLog(request, "website.views.sendFeedBack")
    if request.is_ajax():
        if request.method == 'GET':
            rate = request.GET['rate']
            comment = request.GET['comment']
            mail = request.GET['email']
            if(validateEmail(mail)):
                feed = feedBack(type_feed=rate, email=mail, comment=comment)
                feed.save()
                response = {"feed_id": feed.id}
                # Send Email to staff
                _users = User.objects.filter(is_staff=True)
                staff_emails = []
                for i in _users:
                    staff_emails.append(i.email)
                if rate == '0':
                    type_feed = 'General'
                elif rate == '1':
                    type_feed = 'Sugerencia'
                elif rate == '2':
                    type_feed = 'Error'
                elif rate == '3':
                    type_feed = 'Pregunta'
                else:
                    type_feed = 'No definido'

                ctx_email = {
                    'type_feed': type_feed,
                    'email': mail,
                    'comment': comment,
                }
                sendEmailHtml(9, ctx_email, staff_emails)
            else:
                response = {"error": "Correo invalido"}
            return HttpResponse(json.dumps(response), mimetype="application/json")
    else:
        return HttpResponseRedirect("/")
    return True


@login_required(login_url='/account/login')
def showFeedBack(request):
    '''
    Visualizacion de comentarios ingresados en Actarium (feedback)
    '''
    saveViewsLog(request, "website.views.showFeedBack")
    if request.user.is_staff:
        _feedBack = feedBack.objects.all().order_by("-date_added")
        return render_to_response('website/feedback.html', {'feeds': _feedBack}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")


def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email):
            return True
        else:
            return False
    else:
        return False


def about(request):
    saveViewsLog(request, "website.views.about")
    return render_to_response('website/about.html', {}, context_instance=RequestContext(request))


def blog(request):
    saveViewsLog(request, "website.views.blog")
    return render_to_response('website/blog.html', {}, context_instance=RequestContext(request))


def help(request):
    saveViewsLog(request, "website.views.help")
    try:
        faqs = faq.objects.filter(is_active=True)
    except faq.DoesNotExist:
        faqs = None
    return render_to_response('website/help.html', {"faqs": faqs}, context_instance=RequestContext(request))


def privacy_(request):
    saveViewsLog(request, "website.views.privacy_")
    try:
        p = privacy.objects.get(is_active=True)
    except privacy.DoesNotExist:
        p = None
    title = u"Políticas de privacidad"
    ctx = {"title": title, "content": p, "privacy": True, "terms": False}
    return render_to_response('website/conditions_privacy.html', ctx, context_instance=RequestContext(request))


def terms(request):
    saveViewsLog(request, "website.views.terms")
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


def services(request):
    # pdf = open(settings.STATIC_URL + "Actarium.pdf", "r")
    pdf = open(settings.STATICFILES_DIRS[0] + "/Actarium.pdf", "r")
    response = HttpResponse(pdf.read(), mimetype='application/pdf')
    response['Content-Disposition'] = 'inline;filename=Services.pdf'
    pdf.close()
    return response