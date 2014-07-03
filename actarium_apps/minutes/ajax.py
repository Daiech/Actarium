from django.http import HttpResponse
from apps.groups_app.models import rol_user_minutes
from actarium_apps.organizations.models import rel_user_group, Groups
from apps.account.templatetags.gravatartag import showgravatar
import json

def get_approving_commission(request, slug_group):
    if True:#request.is_ajax():
        group = Groups.objects.get_group(slug=slug_group)
        members = group.rel_user_group_set.get_all_active()
        rel = group.rol_user_minutes_id_group.filter(id_minutes=None, is_active=False)

        members_list = list()
        for m in members:
            rol = m.id_user.rol_user_minutes_id_user.get_or_none(id_minutes=None, is_active=False)
            members_list.append({
                "id": m.id_user.id,
                "full_name": m.id_user.get_full_name(),
                "img": showgravatar(m.id_user.email, 20),
                "is_active": m.id_user.is_active,
                "role": {
                    "is_president": rol.is_president if rol else False,
                    "is_secretary": rol.is_secretary if rol else False,
                    "is_signer": rol.is_signer if rol else False,
                    "is_approver": rol.is_approver if rol else False,
                    "is_assistant": rol.is_assistant if rol else False,
                    "is_signer": rol.is_signer if rol else False
                }
                })
        response = {"members": members_list}
    else:
        response = {'error': "Not allowed"}
    return HttpResponse(json.dumps(response), mimetype="application/json")