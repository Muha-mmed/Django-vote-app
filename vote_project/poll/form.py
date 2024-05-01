from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class signupform(UserCreationForm):
    email = forms.EmailField(max_length=254,help_text='Required. Enter a valid email address')
     
    class meta:
        model = User
        field = ['username', 'email' ,'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)