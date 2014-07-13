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
from actarium_apps.core.models import LastMinutesTasks
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
def create_task(request):
    
    if not request.is_ajax():
        message = {'error': _( u"No es posible realizar esta acción" )}
        return HttpResponse(json.dumps(message), mimetype="application/json")
    
    # get POST data
    name = request.POST.get("name")
    description = request.POST.get("description")
    responsible  = request.POST.get("responsible")
    due = datetime.datetime.strptime(str(request.POST.get("due")), "%Y-%m-%d").replace(tzinfo=utc)
    minutes = request.POST.get("minutes")

    # get minutes validation
    if not minutes:
        message = {'error': _( u"Es necesario gúardar el acta para agregarle tareas." )}
        return HttpResponse(json.dumps(message), mimetype="application/json")
    try:
        minutes_obj = LastMinutes.objects.get(pk=int(minutes))
    except:
        message = {'error': _( u"Ha ocurrido un error intentando obtener el acta" )}
        return HttpResponse(json.dumps(message), mimetype="application/json")   

    # permission validation - is_secretary
    from apps.groups_app.utils import getRelUserGroup
    _user_rel = getRelUserGroup(request.user, minutes_obj.id_group.id)
    is_org_admin = minutes_obj.id_group.organization.has_user_role(request.user, "is_secretary")

    if not ((_user_rel and _user_rel.is_secretary and _user_rel.is_active) or is_org_admin):
        message = {'error': _( u"No tienes permiso para realizar esta acción" )}
        return HttpResponse(json.dumps(message), mimetype="application/json")
    
    # form validations
    form = createTaskForm({"name":name,"description":description, "responsible":responsible, "due":due})
    if not form.is_valid():
        message = {'form_errors':  dict(form.errors.items()) }
        return HttpResponse(json.dumps(message), mimetype="application/json")
    
    # validate database configuration - fixtures
    status_obj = Status.objects.get_or_none(code="ASI")
    creator_role_obj = Roles.objects.get_or_none(code="CRE")
    responsible_role_obj = Roles.objects.get_or_none(code="RES")
    if not (status_obj and creator_role_obj and responsible_role_obj):
        message = {'error': _( u"Ha ocurrido un error en la plataforma, comunicate con los administradores para solucionarlo" )} 
        return HttpResponse(json.dumps(message), mimetype="application/json")
          
    # create tasks
    task_obj = Tasks.objects.create(name=name,description=description,due=due)
    UserTasks.objects.create(user=request.user,role=creator_role_obj,task=task_obj)
    responsible_obj = User.objects.get(id=responsible)
    UserTasks.objects.create(user=responsible_obj,role=responsible_role_obj,task=task_obj)
    Actions.objects.create(user=responsible_obj, status=status_obj,task=task_obj)
    LastMinutesTasks.objects.create(minutes= minutes_obj,task=task_obj)
    new_task = task_as_json(task_obj)


    message = {'successful': _( "true" ), "new_task": [new_task]} 
    return HttpResponse(json.dumps(message), mimetype="application/json")
        


    