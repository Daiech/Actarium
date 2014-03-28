from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.utils.translation import ugettext as _
from .models import ServicesRanges
import json



@login_required(login_url='/account/login')
def get_total_price(request):
    # saveViewsLog(request, "actarium_apps.organizations.views_ajax.getListMembers")
    if request.is_ajax():
        if request.method == "POST":
            quantity = request.POST.get('quantity')

            if quantity and not quantity=="":
                try:
                    quantity = int(quantity)
                    total_price = ServicesRanges.objects.get_total_price(quantity)
                    if total_price:
                        message = {'quantity': total_price}
                    else:
                        message = {'Error': _( "(No disponible)" )}
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
