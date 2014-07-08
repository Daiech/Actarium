#encoding:utf-8
from apps.account.templatetags.gravatartag import showgravatar

def task_as_json(task_obj):
    new_task = {
                "id":task_obj.id,
                "name":task_obj.name,
                "short_name":task_obj.name[0:45]+"..." if len(task_obj.name) >= 45 else task_obj.name,
                "description":task_obj.description,
                "img":showgravatar(task_obj.responsible.email,40), 
                "responsible":task_obj.responsible.first_name, 
                "color":task_obj.color
                }
    return new_task
