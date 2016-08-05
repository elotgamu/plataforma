from django.contrib import admin
from .models import Suscription

# Register your models here.


# superuser can add suscription type items
admin.site.register(Suscription)
