from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.utils.translation import ugettext as _
from .models import Tasks, Roles, UserTasks, Actions, Status
from .forms import createTaskForm
from django.contrib.auth.models import User
import json
import datetime
from apps.account.templatetags.gravatartag import showgravatar
from actarium_apps.core.models import LastMinutesTasks
from apps.groups_app.models import minutes as LastMinutes

@login_required()
def get_minutes_tasks(request, minutes_id):
    if request.is_ajax():
        tasks_list = Tasks.objects.get_tasks_by_minutes(minutes_id)
        tasks = []
        for task in tasks_list:
            tasks.append({
                "id":task.id,
                "name":task.name,
                "short_name":str(task.name)[0:45]+"..." if len(str(task.name)) >= 45 else task.name,
                "description":task.description,
                "img":showgravatar(task.responsible.email,40), 
                "responsible":task.responsible.first_name, 
                "color":task.color})
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
        due = request.POST.get("due")
        minutes = request.POST.get("minutes")
        print "MINUTESSSSS",minutes

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

                print minutes
                minutes_obj = LastMinutes.objects.get(pk=int(minutes))
                LastMinutesTasks.objects.create(minutes= minutes_obj,task=task_obj)



                print "EStado y roles correctos"
            new_task = {};
            #     "id":task.id,
            #     "name":task.name,
            #     "short_name":str(task.name)[0:45]+"..." if len(str(task.name)) >= 45 else task.name,
            #     "description":task.description,
            #     "img":showgravatar(task.responsible.email,40), 
            #     "responsible":task.responsible.first_name, 
            #     "color":task.color}

            print "Create Tasks",name, description, responsible, due
            message = {'successful': _( "true" ), "new_task": [new_task]} 
        else:
            message = {'errors':  dict(form.errors.items()) }
    else:
        message = {'Error': _( "Error" )}

    print message
    return HttpResponse(json.dumps(message), mimetype="application/json")