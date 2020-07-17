from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .data import *


# Creamos un model manager custom para el base model
# para poder anadir funcionalidades nuevas al ORM
class BaseModelManager(models.Manager):
    def active(self):
        """
        Retorna un queryset con los objetos no eliminados

        :return: Un Queryset
        """
        return self.exclude(deleted_date__isnull=False)


# Modelo base con los campos de auditoria
# El resto hereda de este
class BaseModel(models.Model):
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()
    deleted_date = models.DateTimeField(db_index=True, null=True, blank=True)

    objects = BaseModelManager

    class Meta:
        abstract=True

    # Cada vez que se guarda un modelo, se
    # actualizan los campos de auditoria
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()

        self.updated_date = timezone.now()
        return super(BaseModel, self).save(*args, **kwargs)


# Extendemos el modelo de User de django
class KisaUser(User):
    class Meta:
        proxy = True

    @property
    def is_client(self):
        return self.groups.filter(name=CLIENT_GROUP).exists()

    @property
    def is_driver(self):
        return self.groups.filter(name=DRIVER_GROUP).exists()


# Heredamos del modelo de User para agregar datos
class Person(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    identification = models.CharField(max_length=80)
    birth_date = models.DateField()

    class Meta:
        abstract=True

    def __str__(self):
        return "{} {} ({})".format(
            self.user.first_name,
            self.user.last_name,
            self.identification)


class Client(Person):
    balance = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.user.groups.add(CLIENT_GROUP)
        return super(Client, self).save(*args, **kwargs)

    def add_balance(self, amount, payment_method=None):
        self.balance += amount

    def transfer_balance(self, amount, destinary):
        self.balance -+ amount
        destinary.add_balance(destinary)

    def charge_ticket(self, route):
        self.balance -= route.ticket_price


class PaymentMethod(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)    
    card_number = models.IntegerField()
    card_holder = models.CharField(max_length = 80)
    cv2 = models.IntegerField()
    postal_code = models.IntegerField()

    def __str__(self):
        return "{}".format(
            self.card_number)


class District(BaseModel):
    name = models.CharField(max_length = 80)
    province = models.IntegerField(choices=PROVINCE_CHOICES)

    def __str__(self):
        return "{}, {}".format(
            self.name,
            self.province)


class BusRoute(BaseModel):
    title = models.CharField(max_length = 80)
    ticket_price = models.IntegerField()
    ctp_code = models.IntegerField()
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    payment_successful = models.BooleanField()

    def __str__(self):
        return "{} - {}".format(
            self.ctp_code,
            self.title)


class Driver(Person):
    bus_route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.user.groups.add(DRIVER_GROUP)
        return super(Driver, self).save(*args, **kwargs)

    def __str__(self):
        return "{} {} ({})".format(
            self.user.first_name,
            self.user.last_name,
            self.bus_route)


class BusRouteTicket(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    amount_payed = models.IntegerField()

    def __str__(self):
        return "{} - {} en ruta {}".format(
            self.created_date,
            self.client.identification,
            self.driver.bus_route)
