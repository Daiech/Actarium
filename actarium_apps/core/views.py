#encoding:utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required()
def read_organizations_services(request,slug_org=False):
    if slug_org:
        my_orgs = [request.user.organizationsuser_user.get_org(slug=slug_org)]
        show_all = True
    else:
        my_orgs = request.user.organizationsuser_user.get_orgs_by_role_code("is_creator")
    return render(request,'organizations_services.html', locals())
