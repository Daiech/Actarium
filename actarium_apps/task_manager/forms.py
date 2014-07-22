#encoding:utf-8
from django import forms
from apps.groups_app.validators import validate_date
from django.utils.translation import ugettext_lazy as _

class createTaskForm(forms.Form):
    name = forms.CharField(required=True)
    description = forms.CharField(required=False)
    responsible = forms.CharField()
    due = forms.DateTimeField(input_formats=['%Y-%m-%d'], required=False)