#encoding:utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404

from actarium_apps.customers_services.models import OrderItems


@login_required()
def read_organization_services(request,slug_org):
    if slug_org:
        org = request.user.organizationsuser_user.get_org(slug=slug_org)
        if org and org.has_user_role(request.user,'is_admin'):
            if request.method == "GET":
                order = request.GET.get('order')
                print "ORDER", order
                is_admin = True
                customer_service = org.organizationservices_organization.get_members_service_active()
                customer = request.user.actariumcustomers_user.all()[0].customer
                order_items = OrderItems.objects.filter(customer_service=customer_service, order__customer=customer).order_by('-created')
        return render(request,'organizations_services.html', locals())   
    raise Http404
    



