#encoding:utf-8
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from apps.account.validators import validate_email_unique
from apps.groups_app.models import DNI_type


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Correo Electrónico", validators=[validate_email_unique], widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de Usuario'}),
        help_text="Requerido. 30 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente."
    )

    class Meta:
        model = User
        fields = ("username", "email",)

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["username"]
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    email = forms.EmailField(label="* Correo Electrónico", widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    username = forms.CharField(label="* Nombre de usuario", widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    first_name = forms.CharField(label="* Nombre", widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    last_name = forms.CharField(label="Apellido", required=False, widget=forms.TextInput(attrs={'placeholder': 'Apellido'}))

    class Meta:
        model = User
        unique = ('email')
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self):
        print self.cleaned_data["email"]
        user = super(UserForm, self).save()
        return user

class NewDNI(forms.Form):
    dni_type = DNI_type.objects.all()
    i = 0
    CHOICES = []
    for gt in dni_type:
        CHOICES.append((gt.id, gt.short_name+" ("+gt.long_name+")"))
        i = i + 1
    dni = forms.CharField(label="DNI", widget=forms.TextInput(attrs={'placeholder': 'DNI'}))
    dni_type = forms.ChoiceField(label="Tipo de DNI", choices=CHOICES)

        
        
    
    
    
    
    
    
    
    