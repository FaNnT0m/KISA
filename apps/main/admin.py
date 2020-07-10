from django.contrib import admin
from .models import (
    Client,
    District,
    BusRoute,
    Driver
)

class ClientAdmin(admin.ModelAdmin):
    fields = ('user', 'birth_date')

admin.site.register(Client, ClientAdmin)


class DistrictAdmin(admin.ModelAdmin):
    fields = ('name', 'province')

admin.site.register(District, DistrictAdmin)


class BusRouteAdmin(admin.ModelAdmin):
    fields = ('title', 'ticket_price', 'ctp_code', 'district')

admin.site.register(BusRoute, BusRouteAdmin)


class DriverAdmin(admin.ModelAdmin):
    fields = ('user', 'birth_date', 'bus_route')

admin.site.register(Driver, DriverAdmin)