# Create your views here.
# encoding:utf-8
from django.contrib.auth.decorators import login_required
from apps.actions_log.models import actions, rel_user_action
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pymongo import MongoClient, DESCENDING as pymongo_DESCENDING
#from django.core.mail import EmailMessage
import datetime
import sys
from .utils import connect_to_actarium_db, saveErrorLog
#@login_required(login_url='/account/login')


def saveActionLog(id_user, code, extra, ip_address):
    try:
        action = actions.objects.get(code=code)
        log = rel_user_action(
            id_user=id_user, id_action=action, extra=extra, ip_address=ip_address)
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


@login_required(login_url='/account/login')
def showActions(request):
    saveViewsLog(request, 'actions_log.views.showActions')
    if request.user.is_staff:
        # saveErrorLog('(%s) ingreso al actionlog' % request.user.username)
        actions_list = rel_user_action.objects.all().order_by("-date_done")
        paginator = Paginator(actions_list, 25)
        page = request.GET.get('page')
        try:
            actions = paginator.page(page)
        except PageNotAnInteger:# If page is not an integer, deliver first page.
            actions = paginator.page(1)
        except EmptyPage:# If page is out of range (e.g. 9999), deliver last page of results.
            actions = paginator.page(paginator.num_pages)
        ctx = {"actions": actions}
        return render_to_response('actions/actions.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


@login_required(login_url='/account/login')
def showAction(request, id_action):
    saveViewsLog(request, 'actions_log.views.showAction')
    if request.user.is_staff:
        ctx = {"actions": rel_user_action.objects.filter(
            id_action=id_action).order_by("-date_done")}
        return render_to_response('actions/actions.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


@login_required(login_url='/account/login')
def showUserActions(request, username):
    saveViewsLog(request, 'actions_log.views.showUserActions')
    if request.user.is_staff:
        user = User.objects.get_or_none(username=username)
        ctx = {"actions": rel_user_action.objects.filter(id_user=user).order_by("-date_done")}
        return render_to_response('actions/actions.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


@login_required(login_url='/account/login')
def showOrderActions(request, field):
    saveViewsLog(request, 'actions_log.views.showOrderActions')
    if request.user.is_staff:
        ctx = {
            "actions": rel_user_action.objects.filter().order_by("-%s" % (field))}
        return render_to_response('actions/actions.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


@login_required(login_url='/account/login')
def showUserActionsOrder(request, username, field):
    saveViewsLog(request, 'actions_log.views.showUserActionsOrder')
    if request.user.is_staff:
        if username == "ALL":
            action = rel_user_action.objects.filter().order_by("-%s" % (field))
        else:
            user = User.objects.get(username=username)
            action = rel_user_action.objects.filter(
                id_user=user).order_by("-%s" % (field))
        ctx = {"actions": action}
        return render_to_response('actions/actions.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')





def saveViewsLog(request, page):
    
    db = connect_to_actarium_db()
    print db 
    if db:
        views = db.views
        try:
            if request.user.is_authenticated():
                id_user = request.user.pk
                username = request.user.username
            else:
                id_user = 0
                username = "Anonymous User"
            data = {
                'id_user': id_user,
                'username': username,
                'page': page,
                'date': datetime.datetime.now(),
                'ip': request.META['REMOTE_ADDR']
            }
            views.insert(data)
        except:
            print "Error: %s" % (sys.exc_info()[0])
        return True
    else:
        print "Error con mongodb "
        return False
    
    
    print "Error: No se pudo establecer conexion con MongoDB"
    return False


@login_required(login_url='/account/login')
def showViewsLog(request):
    saveViewsLog(request, 'actions_log.views.showViewsLog')
    if request.user.is_staff:
        try:
            db = connect_to_actarium_db()
            views = db.views
            try:
                if request.method == "GET":
                    u = str(request.GET['u'])
                    count = views_data = views.find({'username': u}).count()
                    views_data = views.find({'username': u}).sort(
                        [("date", pymongo_DESCENDING)])
            except:
                count = views.find().count()
                views_data = views.find().sort([("date", pymongo_DESCENDING)])
            ctx = {"views": views_data, "count": count}
        except:
            ctx = {"views": [], 'count': 0}
        return render_to_response('actions/views.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


def showViewsStats(request):
    saveViewsLog(request, 'actions_log.views.showViewsStats')
    if request.user.is_staff:
        try:
            db = connect_to_actarium_db()
            from bson.code import Code
            _map = Code("function () {"
                        "var key = this.page;"
                        "var values = {'id':key, count: 1 };"
                        "    emit(key,values);"
                        "}")
            _reduce = Code("function (key, values) {"
                           "  var reducedValue = {'id':key,'count':0};"
                           "  for (var i = 0; i < values.length; i++) {"
                           "    reducedValue['count'] += parseInt(values[i].count);"
                           "  }"
                           "  return reducedValue;"
                           "}")
            result_views = db.views.map_reduce(_map, _reduce, "result_views")
            mr = result_views.find()
            data = []
            for i in mr:
                data.append(i)
            ctx = {"views": data}
        except:
            ctx = {"views": []}
        return render_to_response('actions/views_stats.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')
