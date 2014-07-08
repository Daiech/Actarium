from actarium_apps.organizations.models import Groups
from apps.account.templatetags.gravatartag import showgravatar


def get_minutes_roles(minutes, group=None):
    """return a JSON with the users minutes roles. if minutes is None, the param group is needed to know the group"""
    if minutes:
        group = minutes.id_group
    elif not group:
        return False
    members = group.rel_user_group_set.get_all_active().order_by("-id_user__is_active")
    is_active = True if minutes else False
    # rel = group.rol_user_minutes_id_group.filter(id_minutes=minutes, is_active=is_active)

    members_list = list()
    for m in members:
        rol = m.id_user.rol_user_minutes_id_user.get_or_none(id_minutes=minutes, is_active=is_active)
        members_list.append({
            "id": m.id_user.id,
            "username": m.id_user.username,
            "full_name": m.id_user.first_name + " " + m.id_user.last_name[0] + ".",
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

    return members_list
