# Create your views here.
#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from actions_log.models import actions, rel_user_action 
from django.contrib.auth.models import User
#from django.core.mail import EmailMessage

def saveActionLog(id_user,code,extra,ip_address):
    action = actions.objects.get(code=code)
    log = rel_user_action(id_user=id_user, id_action = action, extra=extra, ip_address=ip_address)
    try:
        log.save()
        return True
    except User.DoesNotExist, e:
        print "Error al registrar accion: %s" % e
        return False

