#encoding:utf-8
from django import forms
from apps.groups_app.validators import validate_date
from django.utils.translation import ugettext_lazy as _


class newGroupForm(forms.Form):
    name = forms.CharField(label=_(u"Nombre"), widget=forms.TextInput(attrs={'placeholder': _(u'Nombre del grupo'), 'autofocus': 'autofocus'}))
    description = forms.CharField(label=_(u"Descripción (opcional)"), required=False, widget=forms.TextInput(attrs={'placeholder': _(u'Descripción')}))

   #  class Meta:
   #      model = groups


class newMinutesForm3(forms.Form):
    code = forms.CharField(label=_(u"Codigo"), widget=forms.TextInput(attrs={'placeholder': _(u'Codigo de acta'), 'autofocus': 'autofocus'}))
    date_start = forms.DateTimeField(label=_(u"Fecha inicio"), widget=forms.widgets.DateTimeInput(attrs={'class': 'date-pick'}), input_formats=['%Y-%m-%d %I:%M %p'])
    agenda = forms.CharField(label=_(u"Orden del día"), widget=forms.Textarea(attrs={'placeholder': _(u'Orden del día')}))
    agreement = forms.CharField(label=_(u"Acuerdos"), widget=forms.Textarea(attrs={'placeholder': _(u'Acuerdos')}))


class newMinutesForm(forms.Form):
    TYPES = [(_(u'ORDINARIA'), _(u'ORDINARIA')), (_(u'EXTRAORDINARIA'), _(u'EXTRAORDINARIA'))]
    code = forms.CharField(label=_(u"Codigo"), widget=forms.TextInput(attrs={'placeholder': _(u'Código de acta'), 'autofocus': 'autofocus'}))
    date_start = forms.DateTimeField(label=_(u"Fecha/hora inicio"), localize=True, widget=forms.widgets.DateTimeInput(attrs={'class': 'date-pick', 'placeholder': _(u'Fecha/hora inicio')}), input_formats=['%Y-%m-%d %I:%M %p'])
    date_end = forms.DateTimeField(label=_(u"Fecha/hora finalización"), localize=True, widget=forms.widgets.DateTimeInput(attrs={'class': 'date-pick', 'placeholder': _(u"Fecha/hora finalización")}), input_formats=['%Y-%m-%d %I:%M %p'])
    location = forms.CharField(label=_(u"Lugar"), widget=forms.TextInput(attrs={'placeholder': _(u'Lugar')}))
    agenda = forms.CharField(label=_(u"Orden del día"), widget=forms.Textarea(attrs={'placeholder': _(u'Orden del día')}))
    agreement = forms.CharField(label=_(u"Acuerdos"), widget=forms.Textarea(attrs={'placeholder': _(u'Acuerdos')}))
    type_reunion = forms.ChoiceField(widget=forms.Select(), choices=TYPES)

    extra1 = forms.CharField(initial=" ")
    extra2 = forms.CharField(initial=" ")
    extra3 = forms.CharField(initial=" ")
    


class newReunionForm(forms.Form):
    #formulario para agregar una nueva reunion
    date_reunion = forms.DateTimeField(label=_(u"Fecha"), validators=[validate_date], widget=forms.widgets.DateTimeInput(attrs={'class': 'date-pick', 'placeholder': _(u'Ej: 2013-03-15 02:52 pm')}), input_formats=['%Y-%m-%d %I:%M %p'])
    title = forms.CharField(label=_(u"Título"), widget=forms.TextInput(attrs={'placeholder': _(u'Título')}))
    locale = forms.CharField(label=_(u"Lugar"), widget=forms.TextInput(attrs={'placeholder': _(u'Lugar')}))
    agenda = forms.CharField(label=_(u"Descripción"), widget=forms.Textarea(attrs={'placeholder': _(u'Objetivos de la reunión')}))


class uploadMinutesForm(forms.Form):
    minutesFile = forms.FileField(label=_(u"Archivos"), widget=forms.FileInput(attrs={'multiple': 'multiple', 'accept': 'application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/pdf'}))
