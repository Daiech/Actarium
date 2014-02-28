# encoding:utf-8
from django.shortcuts import render
from groups.models import organizations


def organizations_index(request):
    try:
        orgs = organizations.objects.filter(is_active=True, id_admin=request.user)
    except:
        orgs = None
    # groups = list()
    # for org in orgs:
    #     groups.append({"org": org, "groups_org_list": groups_pro.objects.filter(id_organization=org.id)})
    # ctx = {"organizations": groups, "group_saved": new_group}
    return render(request, "website/index.html", locals())