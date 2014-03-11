# encoding:utf-8
from django.shortcuts import render
from apps.groups_app.models import Organizations as Orgs, Groups


def organizations_index(request):
    try:
        orgs = Orgs.objects.filter(is_active=True, admin=request.user)
    except :
        orgs = None
    # try:
    #     groups = [{"id": 1, "name": "Mi grupo", "num_members": 4}, {"id": 2, "name": "Junta directiva de Parquesoft", "num_members": 43}]
    # except:
    #     groups = None
    organizations = list()
    if orgs:
        for org in orgs:
            organizations.append({"organization": org, "groups": Groups.objects.filter(organization=org)})
    return render(request, "website/index.html", locals())