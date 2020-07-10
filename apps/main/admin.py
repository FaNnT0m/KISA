from django.contrib import admin
from .models import Driver

class DriverAdmin(admin.ModelAdmin):
    fields = ('user','last_login_date')

class DriverAdmin(admin.ModelAdmin):
    exclude = ('birth_date','created_date','updated_date','deleted_date')

admin.site.register(Driver,DriverAdmin)

# Register your models here.
