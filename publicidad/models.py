import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
# Create your models here.


def set_key_expiration():
    """returns the expirations timestamp for the user registration,
    2 days since his/her registration """
    return timezone.now() + datetime.timedelta(2)


class Suscription(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(default=None)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    storage = models.FloatField()
    # no sense
    # max_request = models.IntegerField()

    class Meta:
        verbose_name = "Suscription"
        verbose_name_plural = "Suscriptions"
        db_table = 'suscriptions'

    def __str__(self):
        return self.name


def add_me_to_admin_group(sender, instance, created, **kwargs):
    if created is False:
        if instance.groups.filter(name='Administrator').exists():
            print('This admin already exists in administrator group')
        else:
            admin_group = Group.objects.get(name='Administrator')
            admin_group.user_set.add(instance)
            admin_group.save()
            print('The admin has joined the admin group')


# model for manager of negocios extends django users table
class Administrator(User):
    gender_options = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    )
    gender = models.CharField(max_length=50, choices=gender_options)
    avatar = models.ImageField(upload_to='profiles/',
                               blank=True,
                               null=True,
                               default="static/images/default.jpg")
    activation_key = models.CharField(max_length=50, blank=True, null=True)
    key_expires = models.DateTimeField(default=set_key_expiration)

    class Meta:
        verbose_name = "administrador"
        verbose_name_plural = "administradores"
        db_table = 'administrators'

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

# signal for add an admin to the admin group
post_save.connect(add_me_to_admin_group, sender=Administrator)


def menu_upload_to(instance, filename):
    '''the menu upload path'''
    return 'user_{0}/{1}'.format(instance.owner.id, filename)


class Negocio(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    owner = models.OneToOneField('Administrator', on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.CharField(max_length=8)
    menu_path = models.FileField(upload_to=menu_upload_to, blank=True,
                                 null=True)
    suscription = models.ForeignKey('Suscription', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Negocio"
        verbose_name_plural = "Negocios"
        db_table = 'negocios'

    def get_absolute_url(self):
        return reverse('detalle-negocio', args=[str(self.id)])

    def __str__(self):
        return self.name


# model for customer extends django users table
class Customer(User):
    gender_options = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    )
    gender = models.CharField(max_length=50, choices=gender_options)
    avatar = models.ImageField(upload_to='profiles/',
                               blank=True,
                               null=True,
                               default="static/images/default.jpg")
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=8)
    activation_key = models.CharField(max_length=50, blank=True, null=True)
    key_expires = models.DateTimeField(default=set_key_expiration)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        db_table = 'customers'

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Mesa(models.Model):
    number = models.CharField(max_length=50)
    available = models.BooleanField()
    negocio = models.ForeignKey('Negocio', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
        db_table = 'mesas'

    def __str__(self):
        return self.number


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    negocio = models.ForeignKey('Negocio', on_delete=models.CASCADE,
                                blank=True,
                                null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        db_table = 'products'

    def __str__(self):
        return self.name


class Request(models.Model):
    date = models.DateTimeField()
    delivered_address = models.CharField(max_length=200)
    stored_by = models.CharField(max_length=100)
    delivered = models.BooleanField()
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    negocio = models.ForeignKey('Negocio', on_delete=models.CASCADE)
    details = models.ManyToManyField(
        Product,
        through='request_details',
        through_fields=('request', 'product'))

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        db_table = 'requests'

    def __str__(self):
        return self.id


class request_details(models.Model):
    request = models.ForeignKey('Request', on_delete=models.CASCADE)
    cantidad_producto = models.IntegerField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "detalle_pedido"
        verbose_name_plural = "detalle_pedidos"
        db_table = 'request_details'

    def __str__(self):
        pass


class Promotion(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    flyer = models.ImageField(upload_to='promotions/%Y_%m_%d/')
    is_active = models.BooleanField()
    valid_since = models.DateTimeField()
    expires = models.DateTimeField()
    negocio = models.ForeignKey('Negocio', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"
        db_table = 'promotions'

    def __str__(self):
        return self.name


class Reservation(models.Model):
    date = models.DateTimeField()
    customer_quantity = models.IntegerField()
    expired = models.BooleanField()
    negocio = models.ForeignKey('Negocio', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        db_table = 'reservations'

    def __str__(self):
        pass
