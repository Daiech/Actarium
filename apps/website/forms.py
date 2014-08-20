#encoding:utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import OrderedTemplates


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = OrderedTemplates
        fields = ("address_file", "description")