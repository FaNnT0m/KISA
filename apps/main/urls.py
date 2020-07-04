from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


# Se llaman a todas las vistas que se realizaron
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),# vista de registro
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),#vista de login
    path('logout/', auth_views.LogoutView.as_view(template_name='main/logout.html'), name='logout'),
    path('ticket_payment/', views.ticket_payment, name='ticket_payment'),# De ticket
    path('digital_wallet/', views.digital_wallet, name='digital_wallet'),#vista de digital_waller
    path("base/", views.base, name="base"),
    path("reports/", views.reports, name="reports")
]
