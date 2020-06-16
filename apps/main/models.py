from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

PROVINCES = (
    ("1", "San Jose"),
    ("2", "Alajuela"),
    ("3", "Cartago"),
    ("4", "Heredia"),
    ("5", "Guanacaste"),
    ("6", "Puntarenas"),
    ("7", "Limon")
)

DISTRICTS = (
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
    ("12", "San Domingo")
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

class Person(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    last_login_date = models.DateField()

    class Meta:
        abstract=True

class Client(Person):
    balance = models.FloatField()
    def AddBalance(self, amount, payment_method):
         pass
    def TransferBalance(self, destinary):
         pass
    def ChargeTicket(self, route):
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
    province =  models.ChoiceField(province=PROVINCES)
    district =  models.ChoiceField(district=DISTRICTS)


class BusRouteTicket(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)    
    bus_route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
    amount_payed = models.FloatField()

class BaseModel(models.Model):
    created_date = models.DateTimeField(default=timezone.now())
    created_by = models.CharField(max_length = 30)
    updated_date = models.DateTimeField(default=timezone.now())
    updated_by = models.CharField(max_length = 30)
    deleted_date = models.DateTimeField(db_index=True, null=True, blank=True)
    deleted_by = models.CharField(max_length = 30 ,null=True, blank=True)


