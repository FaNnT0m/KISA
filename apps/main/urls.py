from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='main/logout.html'), name='logout'),
    path('ticket_payment/', views.ticket_payment, name='ticket_payment'),
    path('digital_wallet/', views.digital_wallet, name='digital_wallet'),
    path("client_reports/", views.client_reports, name="client_reports"),
    path("driver_route/", views.driver_route, name="driver_route"),
    path("card_ticket_payment/", views.card_ticket_payment, name="card_ticket_payment")

]
