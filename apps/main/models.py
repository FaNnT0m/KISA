from django.db import models
from django.contrib.auth.models import User, Group
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


# Agregamos algunos metodos el modelo de User de django
def make_client(self):
    client_group = Group.objects.get(name=CLIENT_GROUP_NAME) 
    self.groups.add(client_group)
    self.save()

User.add_to_class("make_client", make_client)

def make_driver(self):
    driver_group = Group.objects.get(name=DRIVER_GROUP_NAME) 
    self.groups.add(driver_group)
    self.save()

User.add_to_class("make_driver", make_driver)

@property
def is_client(self):
    return self.groups.filter(name=CLIENT_GROUP_NAME).exists()

User.add_to_class("is_client", is_client)

@property
def is_driver(self):
    return self.groups.filter(name=DRIVER_GROUP_NAME).exists()

User.add_to_class("is_driver", is_driver)


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
        if not self.id:
            self.user.make_client()

        return super(Client, self).save(*args, **kwargs)

    def add_balance(self, amount, payment_method=None):
        self.balance += amount

    def transfer_balance(self, amount, destinary):
        self.balance -+ amount
        destinary.add_balance(destinary)

    def charge_ticket(self, driver):
        price = driver.bus_route.ticket_price
        ticket = BusRouteTicket(
            client=self,
            driver=driver,
            ticket_price=price,
            payment_successful=False,
        )
        if self.balance >= price:
            self.balance -= price
            self.save()
            ticket.payment_successful = True

        ticket.save()
        return ticket.payment_successful


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

    def __str__(self):
        return "{} - {}".format(
            self.ctp_code,
            self.title)


class Driver(Person):
    bus_route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id:
            self.user.make_driver()

        return super(Driver, self).save(*args, **kwargs)

    def __str__(self):
        return "{} {} ({})".format(
            self.user.first_name,
            self.user.last_name,
            self.bus_route)


class BusRouteTicket(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    ticket_price = models.IntegerField()
    payment_successful = models.BooleanField()

    def __str__(self):
        return "{} - {} en ruta {}".format(
            self.created_date,
            self.client.identification,
            self.driver.bus_route)
