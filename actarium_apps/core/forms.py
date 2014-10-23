#encoding:utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _

from actarium_apps.customers_services.models import PaymentMethods
from .models import Packages

from .validators import greater_than_or_equal_to_five


def service_name(self):
    return self.service.name
Packages.__unicode__ = service_name

class OrderMembersServiceForm(forms.Form):
    MONTHS = [('3','3'), ('6', '6'), ('9', '9'), ('12', '12'), ('18', '18'), ('24', '24')]
    organization = forms.CharField(label=_(u"Organización"), widget=forms.HiddenInput()) # attrs={'placeholder': _(u'Organización'), 'autofocus': 'autofocus'}
    packages = forms.ChoiceField()
    number_of_months = forms.ChoiceField(label=_(u"Número de meses"), widget=forms.Select(), choices=MONTHS)
    payment_method = forms.ModelChoiceField(label=_(u"Método de pago"), queryset=PaymentMethods.objects.none()) #  widget=forms.TextInput(attrs={'placeholder': _(u'Método de pago')})
    discount = forms.CharField(label=_(u"Código de descuento"), widget=forms.TextInput(attrs={'placeholder': _(u'Código de descuento')}), required=False)

    def __init__(self, *args, **kwargs):
        user_customer = kwargs.pop('user_customer',None)
        super(OrderMembersServiceForm, self).__init__(*args, **kwargs)
        if user_customer:
            self.fields['payment_method'].queryset = user_customer.actariumcustomers_user.all()[0].customer.payment_methods.all()

        from apps.website.views import getGlobalVar
        FREE_PACKAGE_ID = getGlobalVar("FREE_PACKAGE_ID")
        queryset_packages = Packages.objects.filter(is_active = True).exclude(id=FREE_PACKAGE_ID)
        self.fields['packages'] = forms.ModelChoiceField(label=_(u"Paquete"), queryset=queryset_packages, empty_label=None)
            

class PackagesForm(forms.Form):

    def __init__(self, option, *args, **kwargs):
        super(PackagesForm, self).__init__(*args, **kwargs)
        if option == 0:
            queryset_packages = Packages.objects.all()
        else:
            queryset_packages = Packages.objects.filter(is_active = True)
        

        self.fields['packages'] = forms.ModelChoiceField(label=_(u"Paquete"), queryset=queryset_packages, empty_label=None)