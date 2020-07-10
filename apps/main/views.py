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


def register(request):  # hace una solicitud de registro de nombre.
    if request.method == 'POST':  # si se  cumple el motodo POST envie los datos
        form = ClientRegisterForm(request.POST)
        if form.is_valid():  # Si este es valido y cumple con los parametros
            form.save()  # Aqui se guarda
            username = form.cleaned_data.get('username')
            # Se crea la cuenta
            messages.success(request, f'Account created for {username}!')
            return redirect('index')

    else:
        form = ClientRegisterForm()

    # Sino no se cumple, se redenriza
    return render(request, 'main/register.html', {'form': form})


def digital_wallet(request):  # muestra el #hace la solicitud de digital_wallet
    client = request.user.client  # hace la solicitud para dar la respuesta
    if request.method == 'POST':  # si se cumple el motodo POST envie los datos
        # Agrega el balance de la cuenta y lo lleva hasta cuenta # Lo conviente de String a Float
        balance_to_add = float(request.POST['balance_to_add'])
        client.add_balance(balance_to_add)  # agregua el monto al balance
        client.save()  # guarde el monto

    context = {
        'client': client  # se envia el dinero al cliente
    }
    return render(request, 'main/digital_wallet.html', context)


def reports(request):
    client = request.user.client
    values = BusRouteTicket.objects.all().values(
        'created_date', 'amount_payed','bus_route__title').filter(client_id=client.id)

    context = {
        'client': client,
        'values': values

    }
    return render(request, 'main/reports.html', context)
