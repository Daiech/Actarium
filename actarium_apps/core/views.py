#encoding:utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404


@login_required()
def read_organizations_services(request,slug_org):
    if slug_org:
        org = request.user.organizationsuser_user.get_org(slug=slug_org)
        if org and org.has_user_role(request.user,'is_creator'):
            is_creator = True
        return render(request,'organizations_services.html', locals())   
    raise Http404
