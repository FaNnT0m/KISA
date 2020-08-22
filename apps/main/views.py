from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .decorators import *
from .data import *
from apps.main.models import *


def index(request):
    return render(request, 'main/index.html')


@group_required(DRIVER_GROUP_NAME)
def ticket_payment(request):
    values = BusRoute.objects.values('title','ticket_price')
    client = request.user.client

    if request.method == 'POST':
        selected_value_route = request.POST['busroute']
        route_selected_price = BusRoute.objects.get(title=selected_value_route)
        client.charge_ticket(route_selected_price)
        report = BusRouteTicket(client=client, bus_route=route_selected_price,
                                amount_payed=route_selected_price.ticket_price)
        client.save()
        report.save()

    context = {
        'values': values
    }
    return render(request, 'main/ticket_payment.html', context)


@anonymous_required
def register(request):
    if request.method == 'POST':
        form = ClientRegisterForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, f'Account created for {client.user.username}!')
            return redirect('login')

    else:
        form = ClientRegisterForm()

    return render(request, 'main/register.html', {'form': form})


@group_required(CLIENT_GROUP_NAME)
def digital_wallet(request):
    client = request.user.client

    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        balance_to_add = int(request.POST['balance_to_add'])
        if balance_to_add <= 0:
            messages.error(request, f'You must enter a balance to add greater than 0!')
            return redirect('digital_wallet')
        if form.is_valid():
            payment_method = form.save(commit=False)
            payment_method.client = client
            payment_method.save()
            client.add_balance(balance_to_add)
            client.save()
            messages.success(request, f'Transation succesful!')
            return redirect('digital_wallet')

    else:
        form = PaymentMethodForm()

    context = {
        'client': client,
        'form' : form,
    }
    return render(request, 'main/digital_wallet.html', context)


@group_required(CLIENT_GROUP_NAME)
def client_reports(request):
    load_years= BusRouteTicket.objects.values_list('created_date__year',flat=True).distinct()
    client = request.user.client
    tickets = ""
    if request.method == 'POST':
        year = request.POST['years']
        month = request.POST['months']
        tickets = BusRouteTicket.objects.all().filter(client_id=client.id, payment_successful=True, created_date__month=month, created_date__year=year)
        if tickets.count() < 1:
            messages.info(request, f'You had no trips in the selected time period')

    context = {
        'client': client,
        'tickets': list(tickets),
        'load_years': list(load_years) 
    }
    return render(request, 'main/client_reports.html', context)


@group_required(DRIVER_GROUP_NAME)
def driver_route(request):
    driver = request.user.driver
    tickets = BusRouteTicket.objects.all().filter(driver_id=driver.id)
    if request.method == 'POST':
        client_identification = request.POST['client_identification']
        client = Client.objects.all().filter(identification=client_identification).first()
        if not client:
            messages.error(request, f'No client with identification "{client_identification}" found!')

        else:
            if client.charge_ticket(driver):
                messages.success(request, f'Client charged succesfully!')
            else:
                messages.error(request, f'Client had insuficient funds!')

    if 'date' in request.GET:
        date = request.GET['date']
        tickets = tickets.filter(created_date__date=date)
        if tickets.count() < 1:
            messages.info(request, f'You had no passengers in the selected day')

    context = {
        'driver': driver,
        'tickets': list(tickets)
    }
    return render(request, 'main/driver_route.html', context)
