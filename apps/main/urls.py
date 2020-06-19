from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home, name='home'),
    path("home/register/",views.register, name="register"),
    path("principal/",views.principal, name="principal")
]
