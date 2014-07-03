from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.utils.translation import ugettext as _
from .models import Tasks
import json
import datetime
from apps.account.templatetags.gravatartag import showgravatar

@login_required()
def get_minutes_tasks(request, minutes_id):
    # if request.is_ajax():
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

    # else:
    #     message = {'Error': _( "Error" )}
        
    return HttpResponse(json.dumps(message), mimetype="application/json")
