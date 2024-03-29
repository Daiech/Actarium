#encoding:utf-8
from apps.account.templatetags.gravatartag import showgravatar

def task_as_json(task_obj):
    title_max_length = 25
    description_max_length = 52
    consulted=[]
    informed=[]

    accountable = None
    if task_obj.accountable:
        accountable = {
        "img":showgravatar(task_obj.accountable.email,25), 
        "name":task_obj.accountable.first_name, 
        "id":task_obj.accountable.id, 
    }

    for user in task_obj.consulted:
        consulted.append({
            "img":showgravatar(user.email,25),
            "name":user.first_name,
            "id":user.id
            })

    for user in task_obj.informed:
        informed.append({
            "img":showgravatar(user.email,25),
            "name":user.first_name,
            "id":user.id
            })

    new_task = {
                "id":task_obj.id,
                "title":task_obj.name,
                "short_title":task_obj.name[0:title_max_length]+"..." if len(task_obj.name) >= title_max_length else task_obj.name,
                "description":task_obj.description,
                "short_description":task_obj.description[0:description_max_length]+"..." if task_obj.description and (len(task_obj.description) >= description_max_length) else task_obj.description,
                "responsible_img":showgravatar(task_obj.responsible.email,25), 
                "responsible":task_obj.responsible.first_name, 
                "responsible_id":task_obj.responsible.id, 
                "accountable": accountable,
                "consulted":consulted,
                "informed":informed,
                "creator":task_obj.creator.first_name, 
                "creator_img":showgravatar(task_obj.creator.email,25),
                "color":task_obj.color,
                "status":task_obj.status,
                "status_code":task_obj.status_code,
                "due":task_obj.due.strftime('%Y-%m-%d') if task_obj.due else ""
    }
    # print  new_task['short_description']
    return new_task
