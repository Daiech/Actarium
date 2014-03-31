#encoding:utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from .models import *
from actarium_apps.core.models import Packages
from actarium_apps.core.forms import OrderMembersServiceForm

@login_required()
def read_pricing(request, slug_org):
    if slug_org:
        org = request.user.organizationsuser_user.get_org(slug=slug_org)
        if org and org.has_user_role(request.user,'is_creator'):
            is_creator = True

        packages = Packages.objects.get_all_active().order_by('code')

        S000 = Services.objects.get_or_none(code='S000')
        S001 = Services.objects.get_or_none(code='S001')
        S002 = Services.objects.get_or_none(code='S002')
        S003 = Services.objects.get_or_none(code='S003')
        S004 = Services.objects.get_or_none(code='S004')
        S005 = Services.objects.get_or_none(code='S005')
        S006 = Services.objects.get_or_none(code='S006')

        services_categories = ServicesCategories.objects.filter(is_active=True)

        order_members_form  = OrderMembersServiceForm(initial={"organization":org.id,"payment_method":'1'})
        order_members_form.fields['payment_method'].queryset = request.user.actariumcustomers_user.all()[0].customer.payment_methods.all()
        # order_members_form.fields['payment_method'].defaults = "1"

        return render(request,'pricing.html', locals())
    raise Http404


