from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Person(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    last_login_date = models.DateField()

    class Meta:
        abstract=True

class Client(Person):
    balance = models.FloatField()
    def AddBalance(amount: int, PaymentMethod: payment_method):
         pass
    def TransferBalance(Client: destinary):
         pass
    def ChargeTicket(BusRoute: route):
        pass

class PaymentMethod(BaseModel):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)    
    card_number = models.IntegerField()
    card_holder = models.CharField(max_length = 80)
    cv2 = models.IntegerField()
    postal_code = models.IntegerField()

class Driver(Person):
    pass
class BusRoute(BaseModel):
    title =  models.CharField(max_length = 80)
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE)
    ticket_price = models.FloatField()
    ctp_code = models.IntegerField()
    province =  models.CharField(max_length = 30)
    district =  models.CharField(max_length = 30)


class BusRouteTicket(BaseModel):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)    
    bus_route = models.OneToOneField(BusRoute, on_delete=models.CASCADE)
    amount_payed = models.FloatField()

class BaseModel(models.Model):
    created_date = models.DateTimeField()
    created_by = models.CharField(max_length = 30)
    updated_date = models.DateTimeField()
    updated_by = models.CharField(max_length = 30)
    deleted_date = models.DateTimeField()
    deleted_by = models.CharField(max_length = 30)


