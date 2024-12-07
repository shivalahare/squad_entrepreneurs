from django import forms
from django.contrib.auth.models import User

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    email = forms.EmailField(required=True, label="Email")
    username = forms.CharField(max_length=150, required=True, label="Username")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
