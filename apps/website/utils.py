# encoding:utf-8
from django.shortcuts import render
from apps.groups_app.models import organizations as Orgs, groups_pro


def organizations_index(request):
    try:
        orgs = Orgs.objects.filter(is_active=True, id_admin=request.user)
    except :
        orgs = None
    # try:
    #     groups = [{"id": 1, "name": "Mi grupo", "num_members": 4}, {"id": 2, "name": "Junta directiva de Parquesoft", "num_members": 43}]
    # except:
    #     groups = None
    organizations = list()
    if orgs:
        for org in orgs:
            organizations.append({"organization": org, "groups": groups_pro.objects.filter(id_organization=org)})
    return render(request, "website/index.html", locals())