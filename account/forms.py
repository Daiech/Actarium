from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

    
class RegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email",widget=forms.TextInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ("username", "email",)
        widgets = {  
            #"username": TextInput(attrs={"placeholder": "username"}),
            #"password": forms.PasswordInput(attrs={"placeholder":"password"})
        }
        
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    