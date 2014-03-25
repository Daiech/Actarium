from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import *


@login_required()
def read_pricing(request, slug_org):
    if slug_org:
        org = request.user.organizationsuser_user.get_org(slug=slug_org)
        if org and org.has_user_role(request.user,'is_creator'):
            is_creator = True
        services_categories = ServicesCategories.objects.filter(is_active=True)
        return render(request,'pricing.html', locals())
    raise Http404


