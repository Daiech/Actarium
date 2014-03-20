#encoding:utf-8
from django import forms
from .models import Organizations


class OrganizationForm(forms.ModelForm):
    name = forms.CharField(label="Nombre de Organización", widget=forms.TextInput(attrs={'placeholder': 'Nombre de organización', 'autofocus': 'autofocus'}))
    description = forms.CharField(label="Descripción (opcional)", required=False, widget=forms.TextInput(attrs={'class': '', 'placeholder': 'Descripción'}))
    image_path = forms.FileField(label="Logo (opcional)", required=False, widget=forms.FileInput(attrs={'placeholder': 'URL del logo'}))

    class Meta:
        model = Organizations
        fields = ("name", "description", "image_path")