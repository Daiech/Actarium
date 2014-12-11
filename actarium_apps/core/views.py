#encoding:utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404

from actarium_apps.customers_services.models import OrderItems

from itertools import chain

@login_required()
def read_organization_services(request,slug_org):
    if slug_org:
        org = request.user.organizationsuser_user.get_org(slug=slug_org)
        if org and org.has_user_role(request.user,'is_admin'):
            if request.method == "GET":
                order = request.GET.get('order')
                is_admin = True
                customer_service = org.organizationservices_organization.get_members_service_active()
                customer = request.user.actariumcustomers_user.all()[0].customer
                order_items = OrderItems.objects.filter(customer_service=customer_service, order__customer=customer).order_by('-created')
        return render(request,'organizations_services.html', locals())   
    raise Http404
    

@login_required()
def search_minutes(request):
    from apps.groups_app.models import minutes, minutes_type_1
    from actarium_apps.organizations.models import OrganizationsUser
    from .utils import *
    # get my minutes
    groups_list = []
    my_orgs = OrganizationsUser.objects.filter(user=request.user, role__code="is_member")
    for org in my_orgs:
        groups = org.organization.get_groups()
        for group in groups:
            groups_list.append(group.id)

    search_text = request.POST.get('search_text')

    # queryset for filter code and group name
    minutes_qs = minutes.objects.filter(id_group__in=groups_list)
    entry_query_1 = get_query(str(search_text), ['code','id_group__name'])
    minutes_list_1 = minutes_qs.filter(entry_query_1)

    # queryset for location, agreement and agenda
    entry_query_2 = get_query(str(search_text), ['location','agreement','agenda'])
    minutes_type_1_qs = minutes_type_1.objects.filter(entry_query_2)
    minutes_list_2 = minutes_qs.filter(id_template__id_type__id=1,id_extra_minutes__in=minutes_type_1_qs)

    minutes_list = set(list(chain(minutes_list_1,minutes_list_2)))

    return render(request,'search_minutes.html', locals())   

