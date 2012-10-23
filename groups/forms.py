#encoding:utf-8
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from groups.models import groups,group_type
from django.db import models
from django.contrib.admin import widgets # para incluir el datapicker
from django.forms import extras
import datetime


class newGroupForm(forms.Form):
    name = forms.CharField(label = "Nombre",widget=forms.TextInput(attrs={'placeholder': 'Nombre del grupo'}))
    description = forms.CharField(label = "Descripción",widget=forms.Textarea(attrs={'placeholder': 'Descripción'}))
    id_group_type = forms.ModelChoiceField(label = "Tipo de Grupo",queryset=group_type.objects.all())
    
#    class Meta:
#        model = groups
#    
#    def save(self,*args, **kwargs):
#        super(groups, self).save(*args, **kwargs)
#        return True
    
class newMinutesForm(forms.Form): 
    #formulario generico para cualquier tipo de acta
    code = forms.CharField(label = "Codigo",widget=forms.TextInput(attrs={'placeholder': 'Codigo de acta'}))
    #configuracion para campos de hora
    format_valid=['%I:%M %p']
    time_widget = forms.widgets.TimeInput(attrs={'class': 'time-pick'})
    #formulario personalizado para un tipo de acta especifico para esta version es el unico tipo
    date_start = forms.TimeField(label = "Hora de Inicio", widget=time_widget, input_formats=format_valid)
    date_end = forms.TimeField(label = "Hora de finalización", widget=time_widget, input_formats=format_valid)
    location = forms.CharField(label = "lugar",widget=forms.TextInput(attrs={'placeholder': 'Lugar'}))
    agenda = forms.CharField(label = "Orden del día",widget=forms.Textarea(attrs={'placeholder': 'Orden del día'}))
    agreement = forms.CharField(label = "Acuerdos",widget=forms.Textarea(attrs={'placeholder': 'Acuerdos'}))
    