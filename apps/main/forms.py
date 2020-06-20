
from django import forms
from django.contrib.auth.models import User
from .models import Person, PaymentMethod


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


class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = [
            'card_number',
            'card_holder',
            'cv2',
            'postal_code'
        ]

    def clean(self):
        cleaned_data = super().clean()

        if len(cleaned_data['cv2']) != 3:
            self.add_error('cv2', 'This field is required')

