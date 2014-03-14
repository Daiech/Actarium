# encoding:utf-8
from django.shortcuts import render
from apps.groups_app.models import Organizations as Orgs, Groups


def organizations_index(request):
    organizations = Orgs.objects.filter(is_active=True, admin=request.user)
    return render(request, "groups_app/read_orgs.html", locals())