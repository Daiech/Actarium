#encoding:utf-8
from django import forms
from apps.groups_app.validators import validate_date
from django.utils.translation import ugettext_lazy as _
# from .models import 

class createTaskForm(forms.Form):

    name = forms.CharField(required=True)
    description = forms.CharField(required=False)
    responsible = forms.CharField()
    accountable = forms.CharField(required=False)
    consulted = forms.CharField(required=False)
    informed = forms.CharField(required=False)
    due = forms.DateTimeField(input_formats=['%Y-%m-%d'], required=False)

    # responsible = forms.ModelMultipleChoiceField(label="Responsables", queryset=queryset_responsable,  widget= forms.SelectMultiple(attrs={'class': 'chosen-select', 'data-placeholder':"Selecciona los responsables"}))