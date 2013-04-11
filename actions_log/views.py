# Create your views here.
#encoding:utf-8
from django.contrib.auth.decorators import login_required
from actions_log.models import actions, rel_user_action
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from pymongo import MongoClient, DESCENDING as pymongo_DESCENDING
#from django.core.mail import EmailMessage
import datetime
import sys
#@login_required(login_url='/account/login')
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


@login_required(login_url='/account/login')
def showActions(request):
    if request.user.is_staff:
        saveErrorLog('(%s) ingreso al actionlog' % request.user.username)
        ctx = {"actions": rel_user_action.objects.all().order_by("-date_done")}
        return render_to_response('actions/actions.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


@login_required(login_url='/account/login')
def showAction(request, id_action):
    if request.user.is_staff:
        ctx = {"actions": rel_user_action.objects.filter(id_action=id_action).order_by("-date_done")}
        return render_to_response('actions/actions.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


@login_required(login_url='/account/login')
def showUserActions(request, username):
    if request.user.is_staff:
        user = User.objects.get(username=username)
        ctx = {"actions": rel_user_action.objects.filter(id_user=user).order_by("-date_done")}
        return render_to_response('actions/actions.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


@login_required(login_url='/account/login')
def showOrderActions(request, field):
    if request.user.is_staff:
        ctx = {"actions": rel_user_action.objects.filter().order_by("-%s" % (field))}
        return render_to_response('actions/actions.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


@login_required(login_url='/account/login')
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

def saveErrorLog(errordata):
    try:
        logfile = open("error.log", "a")
        try:
            logfile.write('%s %s \n'%(datetime.datetime.now(),errordata))
        finally:
            logfile.close()
    except IOError:
        pass
    
def saveViewsLog(request,page):
    try:
        connection = MongoClient('localhost',27017)
        db = connection.actarium
        views = db.views
        try:
            if request.user.is_authenticated():
                id_user = request.user.pk
                username = request.user.username
            else:
                print "usuario anonimo"
                id_user = 0
                username = "Anonymous User"
            data = {
                    'id_user':id_user,
                    'username':username,
                    'page': page,
                    'date': datetime.datetime.now(),
                    'ip': request.META['REMOTE_ADDR']
                    }
            views.insert(data)
        except:
            print "Error: %s"%(sys.exc_info()[0])
        
        return True
    except:
        saveErrorLog("Error: conexion a MongoDB")
        print "Error saveViewsLog"
        return False
    
@login_required(login_url='/account/login')
def showViewsLog(request):
    if request.user.is_staff:
        try:
            connection = MongoClient('localhost',27017)
            db = connection.actarium
            views = db.views
            views_data = views.find().sort([("date", pymongo_DESCENDING)])
#            data = []
#            print " \n ------------Data------------------ \n"
#            for v in views_data:
#                print v
#            print "\n------------------------------------------------\n"
            ctx = {"views": views_data}
        except:
            ctx = {"views": []}
        return render_to_response('actions/views.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')
    
def showViewsStats(request):
    if request.user.is_staff:
        try:
            connection = MongoClient('localhost',27017)
            db = connection.actarium
            views = db.views
            views_data = views.find().sort([("date", pymongo_DESCENDING)])
            
            from bson.code import Code
            map = Code("function () {"
                    "var key = this.page;"
                    "var values = {'id':key, count: 1 };"
                    "    emit(key,values);"
                   "}")
            reduce = Code("function (key, values) {"
                       "  var reducedValue = {'id':key,'count':0};"
                       "  for (var i = 0; i < values.length; i++) {"
                       "    reducedValue['count'] += parseInt(values[i].count);"
                       "  }"
                       "  return reducedValue;"
                      "}")
            result_views = db.views.map_reduce(map, reduce, "result_views")
            mr = result_views.find()
            data = []
            print " \n ------------MapReduce------------------ \n"
            for i in mr:
                data.append(i)
                print "\n------------------------------------------------\n",i    
            
#            data = []
#            print " \n ------------Data------------------ \n"
#            for v in views_data:
#                print v
#            print "\n------------------------------------------------\n"
            ctx = {"views": data}
        except:
            ctx = {"views": []}
        return render_to_response('actions/views_stats.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    