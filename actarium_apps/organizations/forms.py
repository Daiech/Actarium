#encoding:utf-8
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from .models import Organizations
from django.utils.translation import ugettext_lazy as _


class OrganizationForm(forms.ModelForm):
    name = forms.CharField(label="Nombre de Organización",max_length=100,  widget=forms.TextInput(attrs={'placeholder': 'Nombre de organización', 'autofocus': 'autofocus'}))
    description = forms.CharField(label="Descripción (opcional)", max_length=100, help_text=_(u'Máx. 100 caractéres.'), required=False, widget=forms.TextInput(attrs={'class': '', 'placeholder': 'Descripción'}))
    image_path = forms.FileField(label="Logo (opcional)", required=False, widget=forms.FileInput(attrs={'placeholder': _('URL del logo')}), help_text=_("No seleccionar para conservar el actual"))

    def clean_name(self):
    	name = self.cleaned_data.get('name')
    	if name in settings.RESERVED_WORDS:
    		print "ESTE NOMBRE NO SE PUEDE PONER"
    		raise ValidationError(_(u"No puedes usar este nombre para tu organización."))
    	return name

    class Meta:
        model = Organizations
        fields = ("name", "description", "image_path")