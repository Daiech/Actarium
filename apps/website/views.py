# encoding:utf-8
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from django.template import RequestContext
from django.utils import translation
from django.conf import settings
from django.db.models import Sum

from apps.groups_app.models import reunions, assistance, DNI_permissions
from apps.groups_app.utils_meetings import date_time_format_form
from apps.actions_log.views import saveActionLog, saveViewsLog
from apps.emailmodule.views import sendEmailHtml
from apps.account.templatetags.gravatartag import showgravatar
from actarium_apps.customers_services.models import OrderItems, Services
from .models import *
import datetime
import json
import re

def home(request):
    if request.method == "GET" and 'lang' in request.GET:
        try:
            lang_available = False
            for l in settings.LANGUAGES:
                if request.GET.get("lang") in l:
                    lang_available = True
            if lang_available:
                request.session['django_language'] = request.GET.get("lang")
                translation.activate(request.GET.get("lang"))
            else:
                ctx["no_supported"] = True
        except Exception, e:
            print e
    if request.user.is_authenticated():
        saveViewsLog(request, "Home_authenticated")
        from actarium_apps.organizations.views import listOrgs
        return listOrgs(request)
    else:
        return landing(request)


def landing(request):
    saveViewsLog(request, "landing anonymous")
    return render(request, 'website/landing.html')


@login_required
def users(request):
    if request.user.is_staff:
        all_users = User.objects.all()
        active_users = User.objects.get_all_active()
        inactive_users = User.objects.filter(is_active=False)
        orders = OrderItems.objects.exclude(service__code="S000").filter(is_active=True)
        orders_count = orders.aggregate(total=Sum("order_quantity"))
    return render(request, 'website/num_users.html', locals())


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
                    type_feed = _(u'General')
                elif rate == '1':
                    type_feed = _(u'Sugerencia')
                elif rate == '2':
                    type_feed = _(u'Error')
                elif rate == '3':
                    type_feed = _(u'Pregunta')
                else:
                    type_feed = _(u'No definido')

                ctx_email = {
                    'type_feed': type_feed,
                    'email': mail,
                    'comment': comment,
                }
                sendEmailHtml(9, ctx_email, staff_emails)
            else:
                response = {"error": _(u"Correo invalido")}
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


def pricing(request):
    saveViewsLog(request, "website.views.pricing")
    MIN_MONTHLY_PAYMENT = getGlobalVar("MIN_MONTHLY_PAYMENT")
    TRIAL_MEMBERS = getGlobalVar("TRIAL_MEMBERS")
    TRIAL_MONTH = getGlobalVar("TRIAL_MONTH")
    services_list = Services.objects.filter(service_category__code="C001", is_active=True).exclude(code="S000").order_by("-price_per_period")
    return render(request, 'website/pricing.html', locals())


def help(request):
    saveViewsLog(request, "website.views.help")
    try:
        faqs = faq.objects.filter(is_active=True)
    except faq.DoesNotExist:
        faqs = None
    return render(request, 'website/help.html', {"faqs": faqs})


def privacy_(request):
    saveViewsLog(request, "website.views.privacy_")
    try:
        p = privacy.objects.get(is_active=True)
    except privacy.DoesNotExist:
        p = None
    title = _(u"Políticas de privacidad")
    ctx = {"title": title, "content": p, "privacy": True, "terms": False}
    return render(request, 'website/conditions_privacy.html', ctx)


def terms(request):
    saveViewsLog(request, "website.views.terms")
    try:
        t = conditions.objects.get(is_active=True)
    except conditions.DoesNotExist:
        t = None
    title = _(u"Términos y condiciones")
    ctx = {"title": title, "content": t, "privacy": False, "terms": True}
    return render(request, 'website/conditions_privacy.html', ctx)


def getGlobalVar(name):
    try:
        return globalVars.objects.get(name=name).url
    except globalVars.DoesNotExist:
        return ""
    except Exception:
        return ""


def services(request):
    pdf = open(settings.STATICFILES_DIRS[0] + "/pdf/actarium_services.pdf", "r")
    response = HttpResponse(pdf.read(), mimetype='application/pdf')
    response['Content-Disposition'] = 'inline;filename=Services.pdf'
    pdf.close()
    return response


def benefits(request):
    pdf = open(settings.STATICFILES_DIRS[0] + "/pdf/actarium para cliente.pdf", "r")
    response = HttpResponse(pdf.read(), mimetype='application/pdf')
    response['Content-Disposition'] = 'inline;filename=Services.pdf'
    pdf.close()
    return response

@login_required()
def get_initial_data(request):
    data = "You are not welcome here"
    if request.user.is_staff and request.user.is_superuser:
        from actarium_apps.task_manager.models import Status as MyModel
        queryset = MyModel.objects.all()
        from django.core import serializers
        data = serializers.serialize("json", queryset)
    return HttpResponse(data, mimetype="application/json")