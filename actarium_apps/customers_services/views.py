from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import *


@login_required()
def read_pricing(request, slug_org):
    if slug_org:
        org = request.user.organizationsuser_user.get_org(slug=slug_org)
        if org and org.has_user_role(request.user,'is_creator'):
            is_creator = True

        S000 = Services.objects.get_or_none(code='S000')
        S001 = Services.objects.get_or_none(code='S001')
        S002 = Services.objects.get_or_none(code='S002')
        S003 = Services.objects.get_or_none(code='S003')
        S004 = Services.objects.get_or_none(code='S004')
        S005 = Services.objects.get_or_none(code='S005')
        S006 = Services.objects.get_or_none(code='S006')

        services_categories = ServicesCategories.objects.filter(is_active=True)
        return render(request,'pricing.html', locals())
    raise Http404


