from django.http import HttpResponse
from actarium_apps.organizations.models import Groups
from .utils import get_minutes_roles
import json


def get_approving_commission(request, slug_group):
    if request.is_ajax():
        group = Groups.objects.get_group(slug=slug_group)
        members_list = get_minutes_roles(None, group=group)
        response = {"members": members_list}
    else:
        response = {'error': "Not allowed"}
    return HttpResponse(json.dumps(response), mimetype="application/json")