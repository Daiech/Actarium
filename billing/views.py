# encoding:utf-8
from django.contrib.auth.decorators import login_required
from billing.models import *
from groups.models import groups as Groups
# from django.contrib.auth.models import User
from django.shortcuts import render_to_response
# from django.http import HttpResponseRedirect
from django.template import RequestContext
# import datetime


@login_required(login_url='/account/login')
def to_order(request):
    price_customization = PriceCustomization.objects.list_prices()
    price_team_size = PriceTeamSize.objects.list_prices()
    price_advertising = PriceAdvertising.objects.list_prices()
    my_groups = Groups.objects.my_groups(request.user)
    available_months = [3, 6, 9, 12, 18, 24, 32]
    available_weeks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20]
    group = Groups.objects.get(pk=2)
    return render_to_response('to_order.html', locals(), context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def my_products(request):
    pass


@login_required(login_url='/account/login')
def billing_history(request):
    pass


@login_required(login_url='/account/login')
def get_advertising(request):
    pass


@login_required(login_url='/account/login')
def create_advertising(request):
    pass


@login_required(login_url='/account/login')
def show_advertising_stats(request):
    pass
