# Create your views here.
#encoding:utf-8
from django.contrib.auth.decorators import login_required
from actions_log.models import actions, rel_user_action
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
#from django.core.mail import EmailMessage


def saveActionLog(id_user, code, extra, ip_address):
    try:
        action = actions.objects.get(code=code)
        log = rel_user_action(id_user=id_user, id_action=action, extra=extra, ip_address=ip_address)
        log.save()
        return True
    except rel_user_action.DoesNotExist, e:
        print "Error al registrar accion: %s" % e
        return False
    except actions.DoesNotExist, e:
        print "Error al registrar accion: %s" % e
        return False
    except Exception, e:
        print "Error al registrar accion: %s" % e
        return False


def showActions(request):
    if request.user.is_staff:
        ctx = {"actions": rel_user_action.objects.all().order_by("-date_done")}
        return render_to_response('actions/actions.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


def showAction(request, id_action):
    if request.user.is_staff:
        ctx = {"actions": rel_user_action.objects.filter(id_action=id_action).order_by("-date_done")}
        return render_to_response('actions/actions.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


def showUserActions(request, username):
    if request.user.is_staff:
        user = User.objects.get(username=username)
        ctx = {"actions": rel_user_action.objects.filter(id_user=user).order_by("-date_done")}
        return render_to_response('actions/actions.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


def showOrderActions(request, field):
    if request.user.is_staff:
        ctx = {"actions": rel_user_action.objects.filter().order_by("-%s" % (field))}
        return render_to_response('actions/actions.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


def showUserActionsOrder(request, username, field):
    if request.user.is_staff:
        if username == "ALL":
            action = rel_user_action.objects.filter().order_by("-%s" % (field))
        else:
            user = User.objects.get(username=username)
            action = rel_user_action.objects.filter(id_user=user).order_by("-%s" % (field))
        ctx = {"actions": action}
        return render_to_response('actions/actions.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')
