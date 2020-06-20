from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

# TODO: Tenemos que cambiar estos choices a modelos o int choices
PROVINCE_CHOICES = (
    ("1", "San Jose"),
    ("2", "Alajuela"),
    ("3", "Cartago"),
    ("4", "Heredia"),
    ("5", "Guanacaste"),
    ("6", "Puntarenas"),            
    ("7", "Limon")
)

DISTRICT_CHOICES = (
    ("1","Carmen"), 
    ("2","Merced"),
    ("3", "Hospital"),
    ("4","San Antonio"),
    ("5","Sabanilla"),
    ("6", "Palmares"),
    ("7","San Nicolás"),
    ("8","Tierra Blanca"),
    ("9","Orosi"),
    ("10","Mercedes"),
    ("11","Barva"),
    ("12", "San Domingo"),
    ("13","Liberia"),
    ("14","Nicoya"),
    ("15", "Sámara"),
    ("16","Paquera"),
    ("17","Cóbano"),
    ("18","Guacimal"),
    ("19","Guápiles"),
    ("20","Siquirres"),
    ("21", "La Rita")
)


# Creamos un model manager custom para el base model
# para poder anadir funcionalidades nuevas al ORM
class BaseModelManager(models.Manager):
    def active(self):
        """
        Obtener un queryset con los objetos no eliminados

        :return: Un Queryset
        """
        return self.exclude(deleted_date__isnull=False)


class BaseModel(models.Model):
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()
    deleted_date = models.DateTimeField(db_index=True, null=True, blank=True)

    objects = BaseModelManager

    class Meta:
        abstract=True

    def save(self, *args, **kwargs):
        """
        Cada vez que se guarda un modelo, se actualizan los campos _date
        """
        '''if not self.id:
            self.created_date = timezone.now()
        '''
        self.updated_date = timezone.now()
        return super(BaseModel, self).save(*args, **kwargs)

class Person(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    last_login_date = models.DateField()

    class Meta:
        abstract=True

class Client(Person):
    balance = models.FloatField()

    def add_balance(self, amount, payment_method):
        self.balance += amount

    def transfer_balance(self, amount, destinary):
        self.balance -+ amount
        destinary.add_balance(destinary)

    def charge_ticket(self, route):
        pass

class PaymentMethod(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)    
    card_number = models.IntegerField()
    card_holder = models.CharField(max_length = 80)
    cv2 = models.IntegerField()
    postal_code = models.IntegerField()

class Driver(Person):
    pass

class BusRoute(BaseModel):
    title =  models.CharField(max_length = 80)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    ticket_price = models.FloatField()
    ctp_code = models.IntegerField()
    # TODO: Cambiar a models o integer choices
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES)
    district = models.CharField(max_length=2, choices=DISTRICT_CHOICES)


class BusRouteTicket(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)    
    bus_route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
    amount_payed = models.FloatField()


