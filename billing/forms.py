#encoding:utf-8
from django import forms

class AdvertisingForm(forms.Form):
    name = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'placeholder': 'Nombre', 'autofocus': 'autofocus'}))
    description = forms.CharField(label=u"Descripción", widget=forms.Textarea(attrs={'placeholder': u'Descripción del anuncio'}))
    url = forms.CharField(label=u"URL", widget=forms.Textarea(attrs={'placeholder': 'http://example.com'}))
    image_path = forms.ImageField()
