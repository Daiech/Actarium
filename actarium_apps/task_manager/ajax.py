#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.utils.translation import ugettext as _
from .models import Tasks, Roles, UserTasks, Actions, Status
from .forms import createTaskForm
from django.contrib.auth.models import User
import json
import datetime
from .utils import *
from apps.groups_app.models import minutes as LastMinutes
from django.utils.timezone import utc


@login_required()
def get_minutes_tasks(request, minutes_id):

    if not request.is_ajax():
        message = {'error': _( u"No es posible realizar esta acción" )}
        return HttpResponse(json.dumps(message), mimetype="application/json")

    if minutes_id == "0" or minutes_id == None:
        message = {'error': _( u"No hay tareas para mostrar" )}
        return HttpResponse(json.dumps(message), mimetype="application/json")

    tasks_list = Tasks.objects.get_tasks_by_minutes(minutes_id)
    tasks = []
    for task in tasks_list:
        tasks.append(task_as_json(task))

    message = tasks
    return HttpResponse(json.dumps(message), mimetype="application/json")

@login_required()
def get_task(request):

    task_id = request.GET.get("task_id")
    # print "task_id desde el servidor", task_id
    if not request.is_ajax():
        message = {'error': _( u"No es posible realizar esta acción" )}
        return HttpResponse(json.dumps(message), mimetype="application/json")

    
    if task_id == None or task_id == "":
        message = {'error': _( u"Error obteniendo la tarea" )}
        return HttpResponse(json.dumps(message), mimetype="application/json")        

    task_obj = Tasks.objects.get_or_none(id=task_id)
    if task_obj == None:
        message = {'error': _( u"La tarea no existe" )}
        return HttpResponse(json.dumps(message), mimetype="application/json")        

    message = {'successful': _( "true" ), "task": [task_as_json(task_obj)]} 
    return HttpResponse(json.dumps(message), mimetype="application/json")

@login_required()
def create_task(request):

    if not request.is_ajax():
        message = {'error': _( u"No es posible realizar esta acción" )}
        return HttpResponse(json.dumps(message), mimetype="application/json")
    
    # get POST data
    task_id = request.POST.get("task_id")
    name = request.POST.get("name")
    description = request.POST.get("description")
    responsible  = request.POST.get("responsible")
    due_str = str(request.POST.get("due"))
    due = None if due_str=="" else datetime.datetime.strptime(due_str, "%Y-%m-%d").replace(tzinfo=utc)
    minutes = request.POST.get("minutes")

    # responsible validation
    if responsible == None or responsible == "":
        message = {'error': _( u"Es necesario asignar un responsable a la tarea." )}
        return HttpResponse(json.dumps(message), mimetype="application/json")
    responsible_obj = User.objects.get_or_none(id=responsible)
    if not responsible_obj:
        message = {'error': _( u"Ha ocurrido un problema intentando asignar la tarea al usuario especificado." )}
        return HttpResponse(json.dumps(message), mimetype="application/json")

    # get minutes validation
    if not minutes:
        message = {'error': _( u"Es necesario gúardar el acta para agregarle tareas." )}
        return HttpResponse(json.dumps(message), mimetype="application/json")
    try:
        minutes_obj = LastMinutes.objects.get(id=int(minutes))
    except:
        message = {'error': _( u"Ha ocurrido un error intentando obtener el acta" )}
        return HttpResponse(json.dumps(message), mimetype="application/json")   

    # permission validation - request user is_secretary - responsible is member
    from apps.groups_app.utils import getRelUserGroup
    _user_rel = getRelUserGroup(request.user, minutes_obj.id_group.id)
    is_org_admin = minutes_obj.id_group.organization.has_user_role(request.user, "is_secretary")
    if not ((_user_rel and _user_rel.is_secretary and _user_rel.is_active) or is_org_admin):
        message = {'error': _( u"No tienes permiso para realizar esta acción" )}
        return HttpResponse(json.dumps(message), mimetype="application/json")
    _responsible_rel = getRelUserGroup(responsible_obj, minutes_obj.id_group.id)
    if not (_responsible_rel and _responsible_rel.is_member and _responsible_rel.is_active):
        message = {'error': _( u"Debes asignar la tarea a un usuario que pertenezca a este grupo" )}
        return HttpResponse(json.dumps(message), mimetype="application/json")


    # form validations
    form = createTaskForm({"name":name,"description":description, "responsible":responsible, "due":due})
    if not form.is_valid():
        print "Formulario invalido", dict(form.errors.items())
        message = {'form_errors':  dict(form.errors.items()) }
        return HttpResponse(json.dumps(message), mimetype="application/json")
    

    
    if task_id == "0":
        # create task
        task_obj, response = Tasks.objects.create_task(name, description, responsible_obj, due, minutes_obj, request.user)
        if not task_obj:
            message = {'error': response} 
        else:
            message = {'successful': _( "true" ), "new_task": [task_as_json(task_obj)], "message": response} 
    else:
        # Update task
        task_obj, response = Tasks.objects.update_task(name, description, responsible_obj, due, minutes_obj, request.user,task_id)
        
        if not task_obj:
            message = {'error': response} 
        else:
            message = {'successful': _( "true" ), "new_task": [task_as_json(task_obj)], "message": response, "task_updated": True} 

    
          
    return HttpResponse(json.dumps(message), mimetype="application/json")
        

@login_required()
def set_task_done(request):

    if not request.is_ajax():
        message = {'error': _( u"No es posible realizar esta acción" )}
        return HttpResponse(json.dumps(message), mimetype="application/json")
    
    task_id = request.GET.get("task_id")
    
    # validate if task exist
    task_obj = Tasks.objects.get_or_none(id=task_id)
    if not task_obj:
        message = {'error': _( u"No existe esta tarea" )}
        return HttpResponse(json.dumps(message), mimetype="application/json")

    # validat if the user has permission for set task done
    if not (task_obj.responsible == request.user):
        message = {'error': _( u"No puedes marcar como terminada una tarea de otro usuario" )}
        return HttpResponse(json.dumps(message), mimetype="application/json")

    # set task done
    is_task_done, response = task_obj.set_task_done()

    if not is_task_done:
        message = {'error': response} 
        return HttpResponse(json.dumps(message), mimetype="application/json")

    message = {'successful': _( "true" ), "new_task": [task_as_json(task_obj)], "message": response } 
    return HttpResponse(json.dumps(message), mimetype="application/json")


@login_required()
def set_task_assigned(request):

    if not request.is_ajax():
        message = {'error': _( u"No es posible realizar esta acción" )}
        return HttpResponse(json.dumps(message), mimetype="application/json")
    
    task_id = request.GET.get("task_id")
    
    # validate if task exist
    task_obj = Tasks.objects.get_or_none(id=task_id)
    if not task_obj:
        message = {'error': _( u"No existe esta tarea" )}
        return HttpResponse(json.dumps(message), mimetype="application/json")

    # validat if the user has permission for set task done
    if not (task_obj.responsible == request.user):
        message = {'error': _( u"No puedes marcar como cancelada una tarea de otro usuario" )}
        return HttpResponse(json.dumps(message), mimetype="application/json")

    # set task done
    is_task_assigned, response = task_obj.set_task_assigned()

    if not is_task_assigned:
        message = {'error': response} 
        return HttpResponse(json.dumps(message), mimetype="application/json")

    message = {'successful': _( "true" ), "new_task": [task_as_json(task_obj)], "message": response } 
    return HttpResponse(json.dumps(message), mimetype="application/json")


@login_required()
def delete_task(request):

    if not request.is_ajax():
        message = {'error': _( u"No es posible realizar esta acción" )}
        return HttpResponse(json.dumps(message), mimetype="application/json")
    
    # get GET data
    task_id = request.GET.get("task_id")

    # verify if task exist
    task_obj, response = Tasks.objects.delete_task(task_id,request.user)

    if not task_obj:
        message = {'error': response }
        return HttpResponse(json.dumps(message), mimetype="application/json")

    message = {'successful': _( "true" ),  "message": response } 
    return HttpResponse(json.dumps(message), mimetype="application/json")