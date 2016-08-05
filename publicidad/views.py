import random
import hashlib
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from .models import Negocio, Administrator, Customer, Suscription
from .forms import negocio_form, admin_form, customer_form, auth_form
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView, ListView, DetailView

from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required

# Create your views here.


class Home(TemplateView):
    """ The home page """
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        return context


class Negocios(ListView):
    """ shows the list of negocios in the app """
    model = Negocio
    template_name = "lista_negocios.html"
    context_object_name = 'negocios'


class NegoDetails(DetailView):
    """ shows the negocio details, tunning needed!"""
    model = Negocio
    template_name = "detalle_negocio.html"
    context_object_name = 'negocio'


def add_negocio(request):
    """ saves a new negocio and its admin in the app """
    if request.method == "POST":
        form_negocio = negocio_form(request.POST, prefix='negocio_form')
        form_admin = admin_form(request.POST, prefix='admin_form')

        if form_negocio.is_valid() and form_admin.is_valid():
            """save the admin id as fk in negocio and its default
            suscription"""
            new_admin = form_admin.save()
            new_negocio = form_negocio.save(commit=False)
            suscription = Suscription.objects.get(name='Free - Prueba')
            new_negocio.suscription = suscription
            new_negocio.owner = new_admin
            new_negocio.save()

            """ now to generate the activation key
            and send email confirmation link"""
            username = form_admin.cleaned_data['username']
            email = form_admin.cleaned_data['email']
            key = set_activation_key(username,
                                     email)

            key_mail_send(request, username, email, key)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Se ha registrado en la plataforma' +
                                 ' revise su correo para activar su cuenta')
            return HttpResponseRedirect('/')

    else:
        form_negocio = negocio_form(prefix='negocio_form')
        form_admin = admin_form(prefix='admin_form')

    return render(request, 'add_negocio.html',
                  {'negocio': form_negocio, 'administrator': form_admin})


def add_customer(request):
    """this uses same funcs for email send activation key as
    administrator function does"""

    if request.method == "POST":
        form_customer = customer_form(request.POST)
        if form_customer.is_valid:
            form_customer.save()

            """ now to generate the activation key
            and send email confirmation link"""
            username = form_customer.cleaned_data['username']
            email = form_customer.cleaned_data['email']

            key = set_activation_key(username,
                                     email)

            key_mail_send(request, username, email, key)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Se ha registrado en la plataforma' +
                                 ' revise su correo para ctivar su cuenta')
            return HttpResponseRedirect('/')

    else:
        form_customer = customer_form()

    return render(request, 'add_customer.html',
                  {'customer': form_customer})


def login_view(request):

    if request.user.is_authenticated():
        # if already login i sould redirec to the undone panel
        pass

    if request.method == "POST":
        form_login = auth_form(request.POST)

        if form_login.is_valid:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)
                # here i should redirect to my undone panel
                """"messages.add_message(request,
                                     messages.SUCCESS,
                                     'Ha iniciado sesion correctamente')
                return HttpResponseRedirect(reverse('home'))"""

            else:
                pass

            pass

    else:
        form_login = auth_form()

    return render(request, 'auth/login.html',
                  {'form': form_login})


def set_activation_key(user_name, email):
    """ generate the activation key for the user """
    salt = hashlib.sha1(str(random.random()).encode('utf-8')
                        ).hexdigest()[:5].encode('utf-8')

    if isinstance(user_name, str):
        user_name = user_name.encode('utf-8')

    key = hashlib.sha1(salt + user_name).hexdigest()

    """ set the generated key in the right Model"""
    if Administrator.objects.filter(username=user_name).exists():
        Administrator.objects.filter(username=user_name
                                     ).update(activation_key=key)
    else:
        Customer.objects.filter(username=user_name
                                ).update(activation_key=key)
    return key


def key_mail_send(request, user_name, email, key):
    """ just send the mail to the provided mail & username
    this needs the request instance to build the full url"""
    url = request.build_absolute_uri(reverse('activate-account',
                                             args=[key]))
    message = ""
    body = render_to_string('emails/new_account_activation_request.html',
                            {
                                'user_name': user_name,
                                'url': url
                            })
    subject = 'Confirmación de la cuenta'

    if subject and body:
        try:
            send_mail(subject,
                      message,
                      settings.EMAIL_HOST_USER,
                      [email],
                      fail_silently=True,
                      html_message=body)
        except BadHeaderError:
            return HttpResponse("Encabezado del mensaje inváido")


def account_confirm(request, key):
    activation_expired = False
    already_active = False
    msm_type = messages.INFO
    msm_message = "Usted ya posee una cuenta y sesion en este sitio"

    if Administrator.objects.filter(activation_key=key).exists():
        """ if the key is for an Admin"""
        user_type = Administrator.objects.get(activation_key=key)
    elif Customer.objects.filter(activation_key=key).exists():
        """ or the key is for a Customer"""
        user_type = Customer.objects.get(activation_key=key)
    else:
        """ this means the user is already active on the site"""
        user_type = None

    if user_type is None:
        already_active = True
    else:
        if timezone.now() > user_type.key_expires:
            # what should do I do? here
            activation_expired = True
            username = user_type.username
            return HttpResponseRedirect(reverse('resend-act-key'),
                                        {'username': username,
                                         'expired': activation_expired}
                                        )
        else:
            user_type.activation_key = ""
            user_type.is_active = True
            user_type.is_staff = True
            user_type.save()
            msm_type = messages.SUCCESS
            msm_message = "Se activado su cuenta, ahora inicie sesion"

    if msm_type and msm_message:
        messages.add_message(request,
                             msm_type,
                             msm_message)

    return render(request, 'home.html',
                  {'active': already_active})


def expired_key(request):
    render(request, 'emails/resend_activation_key_request.html')
