from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.utils.translation import ugettext as _
from .models import ServicesRanges, DiscountCodes
import json
from actarium_apps.core.models import Packages



#@login_required(login_url='/account/login')
def get_total_price(request):
    # saveViewsLog(request, "actarium_apps.organizations.views_ajax.getListMembers")
    if request.is_ajax():
        if request.method == "POST":
            id_package = request.POST.get('id_package')            
            package = Packages.objects.get_or_none(id=id_package)
            if package:
                try:
                    price_per_month = float(package.service.price_per_period)*float(package.number_of_members)
                    message = {'price_per_month': price_per_month}
                    return HttpResponse(json.dumps(message), mimetype="application/json")
                except:
                    message = {'Error': _(" (Introduce un numero)" )}
                    return HttpResponse(json.dumps(message), mimetype="application/json")
            else:
                message = {"Error":  _(" (Introduce un numero)" )}
            return HttpResponse(json.dumps(message), mimetype="application/json")
        else:
            message = False
        return HttpResponse(message, mimetype="application/json")
    else:
        message = False
        return HttpResponse(message, mimetype="application/json")


@login_required(login_url='/account/login')
def get_discount_value(request):
    # saveViewsLog(request, "actarium_apps.organizations.views_ajax.getListMembers")
    if request.is_ajax():
        if request.method == "POST":
            discount_code = request.POST.get('discount_code')
            if discount_code and not discount_code=="":
                discount = DiscountCodes.objects.get_or_none(code=discount_code,is_active=True)
                if discount:
                    discount_value = discount.value
                    message = {'discount_value': discount_value}
                else:
                    message = {'Error': _("(Codigo invalido)" )}
                return HttpResponse(json.dumps(message), mimetype="application/json")
            else:
                message = {'Error': _(u"(Codigo invalido)" )}
            return HttpResponse(json.dumps(message), mimetype="application/json")
        else:
            message = False
        return HttpResponse(message, mimetype="application/json")
    else:
        message = False
        return HttpResponse(message, mimetype="application/json")