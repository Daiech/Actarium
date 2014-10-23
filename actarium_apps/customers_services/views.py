#encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from actarium_apps.core.models import Packages
from actarium_apps.core.models import ServicesRanges
from actarium_apps.core.models import DiscountCodes
from actarium_apps.core.forms import OrderMembersServiceForm

from .models import *



@login_required()
def read_pricing(request, slug_org):
    from apps.website.views import getGlobalVar
        
    if slug_org:
        org = request.user.organizationsuser_user.get_org(slug=slug_org)
        if org and org.has_user_role(request.user,'is_creator'):
            is_creator = True

        id_package = request.GET.get("id_package")
        if id_package:
            show_modal=True
        FREE_PACKAGE_ID = getGlobalVar("FREE_PACKAGE_ID")
        packages = Packages.objects.get_all_active().order_by('code').exclude(id=FREE_PACKAGE_ID)

        services_list = Services.objects.filter(service_category__code="C001", is_active=True).order_by("-price_per_period")

        services_categories = ServicesCategories.objects.filter(is_active=True)

        if request.method == "POST":
            order_members_form = OrderMembersServiceForm(request.POST,user_customer=request.user)
            if order_members_form.is_valid():
                payment_method = order_members_form.cleaned_data['payment_method']
                if payment_method.id == 1:
                    package = order_members_form.cleaned_data['packages']
                    number_of_members = package.number_of_members
                    number_of_months = order_members_form.cleaned_data['number_of_months']
                    discount_code = order_members_form.cleaned_data['discount']
                    customer_services = org.organizationservices_organization.get_members_service_active()
                    service = ServicesRanges.objects.get_service(number_of_members)
                    discount_value_obj = DiscountCodes.objects.get_or_none(code=discount_code,is_active=True)
                    discount_value = discount_value_obj.value if discount_value_obj else  0

                    if int(number_of_months) >= 12:
                        base = float(number_of_members)*service.price_per_period
                        base = base*float(number_of_months)
                        discount_value = discount_value + base*0.05

                    order_id, message = OrderItems.objects.create_members_order(number_of_members=number_of_members,number_of_months=number_of_months,
                                                customer_services=customer_services,service=service,discount_value=discount_value,user=request.user)

                    if order_id:
                        if discount_value_obj:
                            discount_value_obj.is_active= False
                            discount_value_obj.save()
                        return HttpResponseRedirect(reverse("core:read_organization_services",args=(org.slug,))+"?order="+str(order_id))
                    else:
                        error = message
                else:
                    error = _(u"El método de pago seleccionado no existe")
            else:                
                show_modal=True

        else:
            order_members_form  = OrderMembersServiceForm(initial={"organization":org.id,"payment_method":'1',"packages":id_package, "number_of_months": 12 },user_customer=request.user)
            

        return render(request,'pricing.html', locals())
    raise Http404


def read_orders(request):
    order_items = OrderItems.objects.all().order_by("-created")
    return render(request,'admin_orders.html',locals())
