#encoding:utf-8
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from groups.models import groups,group_type
from django.db import models

class newGroupForm(forms.Form):
    name = forms.CharField(label = "Nombre",widget=forms.TextInput(attrs={'placeholder': 'Nombre del grupo'}))
    description = forms.CharField(label = "Descripción",widget=forms.Textarea(attrs={'placeholder': 'Descripción'}))
    id_group_type = forms.ModelChoiceField(queryset=group_type.objects.all())
    
#    class Meta:
#        model = groups
#    
#    def save(self,*args, **kwargs):
#        super(groups, self).save(*args, **kwargs)
#        return True
    