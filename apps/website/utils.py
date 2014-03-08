# encoding:utf-8
from django.shortcuts import render
from apps.groups_app.models import organizations


def organizations_index(request):
    try:
        orgs = organizations.objects.filter(is_active=True, id_admin=request.user)
    except:
        orgs = None
    try:
        groups = [{"id": 1, "name": "Mi grupo", "num_members": 4}, {"id": 2, "name": "Junta directiva de Parquesoft", "num_members": 43}]
    except:
        groups = None
    # groups = list()
    # for org in orgs:
    #     groups.append({"org": org, "groups_org_list": groups_pro.objects.filter(id_organization=org.id)})
    # ctx = {"organizations": groups, "group_saved": new_group}
    return render(request, "website/index.html", locals())