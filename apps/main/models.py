from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# TODO: Seria bueno que dividiesemos las cosas en apps en el futuro


PROVINCE_CHOICES = (
    (1, "San Jose"),
    (2, "Alajuela"),
    (3, "Cartago"),
    (4, "Heredia"),
    (5, "Guanacaste"),
    (6, "Puntarenas"),            
    (7, "Limon"),
)


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


class Person(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()

    class Meta:
        abstract=True


class Client(Person):
    balance = models.FloatField(default=0.0)

    def add_balance(self, amount, payment_method=None): # cuenta con ela aumento y la opcion de abonar/pagar
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


class District(BaseModel):
    name = models.CharField(max_length = 80)
    province = models.IntegerField(choices=PROVINCE_CHOICES)


class BusRoute(BaseModel):
    title = models.CharField(max_length = 80)
    ticket_price = models.IntegerField()
    ctp_code = models.IntegerField()
    district = models.ForeignKey(District, on_delete=models.CASCADE)  


class Driver(Person):
    bus_route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)


class BusRouteTicket(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    amount_payed = models.IntegerField()
