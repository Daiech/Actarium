#encoding:utf-8
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from groups.models import groups
    
class newGroupForm(forms.Form):
    name = forms.CharField(label = "Nombre",widget=forms.TextInput(attrs={'placeholder': 'Nombre del grupo'}))
    description = forms.CharField(label = "Descripción",widget=forms.Textarea(attrs={'placeholder': 'Descripción'}))

    class Meta:
        model = User
        fields = ("username", "email",)
        widgets = {
            #"username": TextInput(attrs={"placeholder": "username"}),
            #"password": forms.PasswordInput(attrs={"placeholder":"password"})
        }
        
    def save(self, commit=True):
        user = super(groups, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    