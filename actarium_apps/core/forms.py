#encoding:utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from actarium_apps.customers_services.models import PaymentMethods
from .validators import greater_than_or_equal_to_five


class OrderMembersServiceForm(forms.Form):
    MONTHS = [('6', '6'), ('9', '9'), ('12', '12'), ('18', '18'), ('24', '24')]
    organization = forms.CharField(label=_(u"Organización"), widget=forms.HiddenInput()) # attrs={'placeholder': _(u'Organización'), 'autofocus': 'autofocus'}
    number_of_members = forms.CharField(label=_(u"Número de miembros"), widget=forms.TextInput(attrs={'placeholder': _(u'Número de miembros')}),validators=[greater_than_or_equal_to_five])
    number_of_months = forms.ChoiceField(label=_(u"Número de meses"), widget=forms.Select(), choices=MONTHS)
    payment_method = forms.ModelChoiceField(label=_(u"Método de pago"), queryset=PaymentMethods.objects.none()) #  widget=forms.TextInput(attrs={'placeholder': _(u'Método de pago')})
    discount = forms.CharField(label=_(u"Código de descuento"), widget=forms.TextInput(attrs={'placeholder': _(u'Código de descuento')}), required=False)

    def __init__(self, *args, **kwargs):
        print 'kwargs',kwargs
        user_customer = kwargs.pop('user_customer',None)
        super(OrderMembersServiceForm, self).__init__(*args, **kwargs)
        if user_customer:
            print user_customer
            self.fields['payment_method'].queryset = user_customer.actariumcustomers_user.all()[0].customer.payment_methods.all()
            