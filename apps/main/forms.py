from datetime import timedelta
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

# Extendemos el UserCreationForm que viene por defecto
# Le agregamos los fields extra de Client
class ClientRegisterForm(UserCreationForm):
    identification = forms.CharField(min_length=9, max_length=9, required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=10, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    birth_date = forms.DateField(widget=forms.TextInput(     
        attrs={'type': 'date'} 
    ), required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'identification',
            'first_name',
            'last_name',
            'birth_date',
            'password1',
            'password2',
        )

    def clean_email(self):
        email = self.cleaned_data['email']
        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            self.add_error('email', 'An user with this email already exists')
        
        return email

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        if birth_date > (timezone.now() - timedelta(days=(365*12))).date():
            self.add_error('birth_date', 'You must be at least 12 years old to use this system')

        return birth_date

    # Sobreescribimos el save para crear primero el User y luego el Client
    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't a new Client & User without commit")

        user = super(ClientRegisterForm, self).save(commit=False)
        user.username = user.email
        user.save()
        client = Client(
            user=user,
            identification=self.cleaned_data['identification'],
            birth_date=self.cleaned_data['birth_date'],
        )
        client.save()
        return client


class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = (
            'card_number',
            'card_holder',
            'cv2',
            'postal_code',
        )

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        if len(str(card_number)) != 16:
            self.add_error('card_number', 'Card numbers must have 16 digits')

        return card_number
   
    def clean_cv(self):        
        cv2 = self.cleaned_data['cv2']
        if len(str(cv2)) !=3:
            self.add_error('cv2', 'Cv2 must have 3 digits')
        return cv2   

    def clean_postal_code(self):
        postal_code=self.cleaned_data['postal_code']
        if len(str(postal_code)) !=3:
            self.add_error('postal_code', 'Postal code must have 3 digits')
        return postal_code

    