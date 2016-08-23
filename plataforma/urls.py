"""plataforma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from publicidad import views

urlpatterns = [
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^agregar_negocio/', views.add_negocio, name='newnegocio'),
    url(r'^account/confirm/(?P<key>\w+)/$', views.account_confirm,
        name='activate-account'),
    url(r'^resend_code_activation/', views.expired_key,
        name='resend-act-key'),
    url(r'^lista_negocios/', views.Negocios.as_view(),
        name='lista-negocios'),
    url(r'^detalles_negocio/(?P<pk>[0-9]+)/$', views.NegoDetails.as_view(),
        name='detalle-negocio'),
    url(r'^agregar_cliente/', views.add_customer, name='newcustomer'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),
]
