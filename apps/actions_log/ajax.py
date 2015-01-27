#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
import json
import datetime
from apps.groups_app.models import minutes as LastMinutes
from django.utils.timezone import utc
from apps.actions_log.utils import create_notification
from apps.account.templatetags.gravatartag import showgravatar
from .models import *


@login_required()
def update_notification(request):
    print "update_notification"

    if not request.is_ajax():
        message = {'error': _( u"No es posible realizar esta acción" )}
        return HttpResponse(json.dumps(message), mimetype="application/json")

    notification_id = request.POST.get('notification_id')
    print "Entro al is_ajax",notification_id

    if notification_id == "0" or notification_id == None:
        message = {'error': _( u"No es valido el id de notificación" )}
        return HttpResponse(json.dumps(message), mimetype="application/json")

    try:
        usernotification = UserNotification.objects.get(id=notification_id)
    except:
        usernotification = None

    if not usernotification:
        message = {'error': _( u"La notificación no existe" )}
        return HttpResponse(json.dumps(message), mimetype="application/json")
    else:
        usernotification.viewed = True
        usernotification.save()
        message = {'error': _( u"Notificación actualizada" )}

    return HttpResponse(json.dumps(message), mimetype="application/json")
