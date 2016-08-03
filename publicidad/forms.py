from django import forms
from django.forms import ModelForm
from .models import Administrator, Customer, Negocio
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class negocio_form(ModelForm):
    class Meta:
        model = Negocio
        fields = ('name',
                  'description',
                  'location',
                  'email',
                  'phone')
        exclude = ['suscription', 'owner']

    """def save(self, commit=False):
        negocio = super(negocio_form, self).save(commit=False)
        suscription_defaults = Suscription.objects.get(name='Free - Prueba')
        negocio.suscription = suscription_defaults
        negocio.save()
        return negocio"""


class admin_form(UserCreationForm):
    """creates a form based on administrator model"""

    class Meta:
        model = Administrator
        fields = [
            "first_name",
            "last_name",
            "gender",
            "username",
            "email"
        ]

    def save(self, commit=True):
        admin = super(admin_form, self).save(commit=False)
        # it works
        admin.is_active = False

        if commit:
            admin.save()
        return admin


class customer_form(UserCreationForm):
    """creates a form based on customer model"""

    class Meta:
        model = Customer
        fields = [
            "first_name",
            "last_name",
            "gender",
            "username",
            "email"
        ]

    def save(self, commit=True):
        customer = super(customer_form, self).save(commit=False)
        customer.is_active = False
        if commit:
            customer.save()
        return customer


class login_form(AuthenticationForm):
    """docstring for login_form"""
    username = forms.CharField(max_length=30,
                               widget=forms.TextInput(attrs={
                                                      'class': 'form-control',
                                                      'name': 'username'
                                                      }))

    password = forms.CharField(max_length=30,
                               widget=forms.PasswordInput(attrs={
                                                    'class': 'form-control',
                                                    'name': 'password'
                                                                }))
