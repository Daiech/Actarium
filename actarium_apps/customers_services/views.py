from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import *


@login_required()
def read_pricing(request):
    services_categories = ServicesCategories.objects.filter(is_active=True)
    return render(request,'pricing.html', locals())
