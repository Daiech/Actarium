#encoding:utf-8
from django import forms
from groups.models import group_type


class newGroupForm(forms.Form):
    name = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'placeholder': 'Nombre del grupo'}))
    description = forms.CharField(label="Descripción", widget=forms.Textarea(attrs={'placeholder': 'Descripción'}))
    id_group_type = forms.ModelChoiceField(label="Tipo de Grupo", queryset=group_type.objects.all())

#    class Meta:
#        model = groups
#
#    def save(self,*args, **kwargs):
#        super(groups, self).save(*args, **kwargs)
#        return True


class newMinutesForm(forms.Form):
    #formulario generico para cualquier tipo de acta
    code = forms.CharField(label="Codigo", widget=forms.TextInput(attrs={'placeholder': 'Codigo de acta'}))
    #configuracion para campos de hora
    format_valid = ['%I:%M %p']
    time_widget = forms.widgets.TimeInput(attrs={'class': 'time-pick'})
    #formulario personalizado para un tipo de acta especifico para esta version es el unico tipo
    date_start = forms.TimeField(label="Hora de Inicio", widget=time_widget, input_formats=format_valid)
    location = forms.CharField(label="Lugar", widget=forms.TextInput(attrs={'placeholder': 'Lugar'}))
    agenda = forms.CharField(label="Orden del día", widget=forms.Textarea(attrs={'placeholder': 'Orden del día'}))
    agreement = forms.CharField(label="Acuerdos", widget=forms.Textarea(attrs={'placeholder': 'Acuerdos'}))
    date_end = forms.TimeField(label="Hora de finalización", widget=time_widget, input_formats=format_valid)


class newReunionForm(forms.Form):
    #formulario para agregar una nueva reunion
    date_reunion = forms.DateTimeField(label="Fecha", widget=forms.widgets.DateTimeInput(attrs={'class': 'date-pick'}), input_formats=['%Y-%m-%d %I:%M %p'])
    agenda = forms.CharField(label="Objetivos", widget=forms.Textarea(attrs={'placeholder': 'Objetivos de la reunión'}))
