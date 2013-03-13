#encoding:utf-8
from django import forms
# from groups.models import group_type
from groups.models import groups
from groups.validators import validate_date

class newGroupForm(forms.Form):
    # group_type = group_type.objects.all()
    # i = 0
    # CHOICES = []
    # print len(group_type)
    # for gt in group_type:
    #     CHOICES.append((gt.id, gt.name))
    #     i = i + 1
    name = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'placeholder': 'Nombre del grupo', 'autofocus': 'autofocus'}))
    description = forms.CharField(label="Descripción", required=False, widget=forms.TextInput(attrs={'placeholder': 'Descripción'}))
    # id_group_type = forms.ChoiceField(label="Tipo de Grupo", choices=CHOICES, widget=forms.RadioSelect(attrs={'class': 'hidden group-type'}))

#    class Meta:
#        model = groups
#
#    def save(self,*args, **kwargs):
#        super(groups, self).save(*args, **kwargs)
#        return True

    # class Meta:
    #     model = groups


class newMinutesForm(forms.Form):
    #formulario generico para cualquier tipo de acta
    code = forms.CharField(label="Codigo", widget=forms.TextInput(attrs={'placeholder': 'Codigo de acta'}))
    #configuracion para campos de hora
    # format_valid = ['%I:%M %p']
    # time_widget = forms.widgets.TimeInput(attrs={'class': 'time-pick'})
    #formulario personalizado para un tipo de acta especifico para esta version es el unico tipo
    date_start = forms.DateTimeField(label="Fecha inicio", widget=forms.widgets.DateTimeInput(attrs={'class': 'date-pick'}), input_formats=['%Y-%m-%d %I:%M %p'])
    location = forms.CharField(label="Lugar", widget=forms.TextInput(attrs={'placeholder': 'Lugar'}))
    agenda = forms.CharField(label="Orden del día", widget=forms.Textarea(attrs={'placeholder': 'Orden del día'}))
    agreement = forms.CharField(label="Acuerdos", widget=forms.Textarea(attrs={'placeholder': 'Acuerdos'}))
    date_end = forms.DateTimeField(label="Fecha finalización", widget=forms.widgets.DateTimeInput(attrs={'class': 'date-pick'}), input_formats=['%Y-%m-%d %I:%M %p'])


class newReunionForm(forms.Form):
    #formulario para agregar una nueva reunion
    date_reunion = forms.DateTimeField(label="Fecha", validators=[validate_date], widget=forms.widgets.DateTimeInput(attrs={'class': 'date-pick'}), input_formats=['%Y-%m-%d %I:%M %p'])
    title = forms.CharField(label="Título", widget=forms.TextInput(attrs={'placeholder': 'Título'}))
    locale = forms.CharField(label="Lugar", widget=forms.TextInput(attrs={'placeholder': 'Lugar'}))
    agenda = forms.CharField(label="Orden del día", widget=forms.Textarea(attrs={'placeholder': 'Objetivos de la reunión'}))



class newOrganizationForm(forms.Form):
    name = forms.CharField(label="Nombre de Organización", widget=forms.TextInput(attrs={'placeholder': 'Nombre de organización', 'autofocus': 'autofocus'}))
    logo_address = forms.FileField(label="Logo", required=False, widget=forms.FileInput(attrs={'placeholder': 'URL del logo'}))
    description = forms.CharField(label="Descripción", required=False, widget=forms.TextInput(attrs={'class': '', 'placeholder': 'Nombre de organización'}))

    # def save(self):
    #     user = super(newOrganizationForm, self).save()
    #     return user

class uploadMinutesForm(forms.Form):
    from groups.validators import validateExtention
    minutesFile = forms.FileField(label="Archivos", widget=forms.FileInput(attrs={'multiple':'multiple','accept':'application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/pdf'}), validators=[validateExtention])
    
