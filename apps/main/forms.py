
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

# Extendemos el UserCreationForm que viene por defecto
# Le agregamos los fields extra de Client
class ClientRegisterForm(UserCreationForm):
    identification = forms.CharField(max_length=9, required=True)
    email = forms.EmailField(required=True) 
    birth_date = forms.DateField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'identification',
            'email',
            'birth_date',
            'password1',
            'password2'
        )

    def validate_identification(self, value):
        if len(value) != 9 or not value.isnumeric():
            raise exceptions.ValidationError(_('Identification must have 9 numbers'))

    # Sobreescribimos el save para crear primero el User y luego el Client
    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't a new Client & User without commit")

        user = super(ClientRegisterForm, self).save(commit=True)
        client = Client(
            user=user,
            identification=self.cleaned_data['identification'],
            birth_date=self.cleaned_data['birth_date'],
        )
        client.save()
        return client


class PaymentMethodForm(forms.ModelForm): # Se crea la clase de forma de pago
    class Meta:
        model = PaymentMethod
        fields = (
            'card_number',
            'card_holder',
            'cv2',
            'postal_code'
        )

    def clean(self):# se limpian los datos
        cleaned_data = super().clean()

        if len(cleaned_data['cv2']) != 3:
            self.add_error('cv2', 'This field is required')# Se comenta que hay datos obligatorios

