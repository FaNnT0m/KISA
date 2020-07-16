from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ClientRegisterForm
from apps.main.models import *

# Son las vistas


def base(request):
    return render(request, 'main/base.html')


def index(request):
    return render(request, 'main/index.html')


def ticket_payment(request):
    # Con 'flat' retorna el set limpio, sin comillas ni parentesis
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


def register(request):
    if request.method == 'POST':
        form = ClientRegisterForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, f'Account created for {client.user.username}!')
            return redirect('index')

    else:
        form = ClientRegisterForm()

    return render(request, 'main/register.html', {'form': form})


def digital_wallet(request):
    client = request.user.client
    if request.method == 'POST':
        balance_to_add = int(request.POST['balance_to_add'])
        client.add_balance(balance_to_add)
        client.save()

    context = {
        'client': client
    }
    return render(request, 'main/digital_wallet.html', context)


def reports(request):
    client = request.user.client
    values = BusRouteTicket.objects.all().values(
        'created_date', 'amount_payed','driver__bus_route__title').filter(client_id=client.id)

    context = {
        'client': client,
        'values': values

    }
    return render(request, 'main/reports.html', context)
