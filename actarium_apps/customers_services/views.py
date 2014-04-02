#encoding:utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

from actarium_apps.core.models import Packages
from actarium_apps.core.models import ServicesRanges
from actarium_apps.core.models import DiscountCodes
from actarium_apps.core.forms import OrderMembersServiceForm

from .models import *



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

        if request.method == "POST":
            order_members_form = OrderMembersServiceForm(request.POST,user_customer=request.user)
            if order_members_form.is_valid():
                payment_method = order_members_form.cleaned_data['payment_method']
                if payment_method.id == 1:
                    number_of_members = order_members_form.cleaned_data['number_of_members']
                    number_of_months = order_members_form.cleaned_data['number_of_months']
                    discount_code = order_members_form.cleaned_data['discount']
                    customer_services = org.organizationservices_organization.get_members_service_active()
                    service = ServicesRanges.objects.get_service(number_of_members)
                    discount_value = DiscountCodes.objects.get_or_none(code=discount_code,is_active=True)
                    discount_value = discount_value.value if discount_value else  0
                    # print "number_of_members",number_of_members
                    # print "number_of_months",number_of_months
                    # print "discount",discount_value
                    # print "customer_services",  customer_services
                    # print "service", service
                    # print "discount_value", discount_value
                    if customer_services and service:
                        customer = request.user.actariumcustomers_user.all()[0].customer
                        if customer:
                            status = OrderStatus.objects.get_or_none(pk=1)
                            if status:
                                # print "STATUS",status
                                customer_orders = CustomerOrders.objects.create(status=status, customer=customer)
                                order_items = OrderItems(service=service,order=customer_orders,order_quantity=number_of_members,number_of_periods=number_of_months,customer_service=customer_services,discount=discount_value)
                                order_items.save()
                            else:
                                print "No Status"
                        else:
                            print "No customer"
                    else:
                        print "No customer services"
                        

                else:
                    error = _("El metodo de pago seleccionado")
            else:                
                show_modal=True

        else:
            order_members_form  = OrderMembersServiceForm(initial={"organization":org.id,"payment_method":'1'},user_customer=request.user)
            

        return render(request,'pricing.html', locals())
    raise Http404

