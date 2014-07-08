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
    if request.is_ajax():
        tasks_list = Tasks.objects.get_tasks_by_minutes(minutes_id)
        tasks = []
        for task in tasks_list:
            tasks.append(task_as_json(task))
        message = tasks

    else:
        message = {'Error': _( "Error" )}
        
    return HttpResponse(json.dumps(message), mimetype="application/json")



@login_required()
def create_task(request):
    if request.is_ajax():
        name = request.POST.get("name")
        description = request.POST.get("description")
        responsible  = request.POST.get("responsible")
        due = datetime.datetime.strptime(str(request.POST.get("due")), "%Y-%m-%d").replace(tzinfo=utc)
        minutes = request.POST.get("minutes")

        form = createTaskForm({"name":name,"description":description, "responsible":responsible, "due":due})
        
       	if form.is_valid():

            status_obj = Status.objects.get_or_none(code="ASI")
            creator_role_obj = Roles.objects.get_or_none(code="CRE")
            responsible_role_obj = Roles.objects.get_or_none(code="RES")

            if status_obj and creator_role_obj and responsible_role_obj:
                task_obj = Tasks.objects.create(name=name,description=description,due=due)
                UserTasks.objects.create(user=request.user,role=creator_role_obj,task=task_obj)
                responsible_obj = User.objects.get(id=responsible)
                UserTasks.objects.create(user=responsible_obj,role=responsible_role_obj,task=task_obj)
                Actions.objects.create(user=responsible_obj, status=status_obj,task=task_obj)

                minutes_obj = LastMinutes.objects.get(pk=int(minutes))
                LastMinutesTasks.objects.create(minutes= minutes_obj,task=task_obj)

                new_task = task_as_json(task_obj)

                message = {'successful': _( "true" ), "new_task": [new_task]} 
            else:
                message = {'Error': _( "Ha ocurrido un error en la plataforma, comunicate con los administradores para solucionarlo" )} 
        else:
            message = {'errors':  dict(form.errors.items()) }
    else:
        message = {'Error': _( "No es posible realizar esta acción" )}

    return HttpResponse(json.dumps(message), mimetype="application/json")