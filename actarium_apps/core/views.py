#encoding:utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required()
def services(request):
    my_orgs = request.user.organizationsuser_user.get_orgs_by_role_code("is_creator")
    return render(request,'services.html', locals())
