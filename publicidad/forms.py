from django import forms
from django.forms import ModelForm
from .models import Administrator, Customer, Negocio
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate


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


class auth_form(AuthenticationForm):
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

    this_login = forms.BooleanField(widget=forms.HiddenInput,
                                    initial=1,
                                    error_messages={
                                        'required': 'Su sesion ha expirado'
                                    })

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        message = forms.ERROR_MESSAGE

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if u'@' in username:
                # Mistakenly entered e-mail address instead of username?
                # Look it up.
                try:
                    user = Administrator.objects.get(email=username)
                except (Administrator.DoesNotExist,
                        Administrator.MultipleObjectsReturned):
                    # Nothing to do here, moving along.
                    pass
                else:
                    if user.check_password(password):
                        message = ("Your e-mail address is not your "
                                   "username."
                                   " Try '%s' instead.") % user.username
                raise forms.ValidationError(message)
            # Removed check for is_staff here!
            elif not self.user_cache.is_active:
                raise forms.ValidationError(message)
        return self.cleaned_data
