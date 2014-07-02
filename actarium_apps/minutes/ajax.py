from django.http import HttpResponse
from apps.groups_app.models import rol_user_minutes
from actarium_apps.organizations.models import rel_user_group, Groups
from apps.account.templatetags.gravatartag import showgravatar
import json

def get_approving_commission(request, slug_group):
    if True:#request.is_ajax():
        group = Groups.objects.get_group(slug=slug_group)
        rel = group.rol_user_minutes_id_group.filter(id_minutes=None, is_active=False)

        members = list()
        for m in rel:
            members.append({
                "id": m.id_user.id,
                "full_name": m.id_user.get_full_name(),
                "img": showgravatar(m.id_user.email, 20),
                "is_active": m.id_user.is_active,
                "role": {
                    "is_approver": m.is_approver,
                    "is_assistant": m.is_assistant,
                    "is_signer": m.is_signer
                }
                })
        response = {"members": members}
    else:
        response = {'error': "Not allowed"}
    return HttpResponse(json.dumps(response), mimetype="application/json")