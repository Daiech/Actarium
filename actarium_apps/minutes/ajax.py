from django.http import HttpResponse
from actarium_apps.organizations.models import Groups
from apps.groups_app.models import minutes
from .utils import get_minutes_roles
import json


def get_approving_commission(request, slug_group, minutes_id=None):
    if request.is_ajax():
        group = Groups.objects.get_group(slug=slug_group)
        if minutes_id:
        	minutes_id = minutes.objects.get_minute(id=minutes_id)
        members_list = get_minutes_roles(minutes_id, group=group)
        response = {"members": members_list}
    else:
        response = {'error': "Not allowed"}
    return HttpResponse(json.dumps(response), mimetype="application/json")