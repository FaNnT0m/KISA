
from django import forms
from django.contrib.auth.models import User
from .models import Person

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        ]

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'birth_date'
        ]
