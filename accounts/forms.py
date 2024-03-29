from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=256, required=True, help_text='Required')
    class Meta:
        model = User
        fields = ('email','username','password1','password2')