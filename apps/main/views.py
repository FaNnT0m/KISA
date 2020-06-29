from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ClientRegisterForm
from apps.main.models import *


def base(request):
    return render(request,'main/base.html')

def index(request):
    return render(request,'main/index.html')

def ticket_payment(request):
    route= BusRoute.objects.values_list('title',flat=True) #Con 'flat' retorna el set limpio, sin comillas ni parentesis
    ticket =BusRoute.objects.values_list('ticket_price',flat=True)
    client = request.user.client

    if request.method == 'POST':
        selected_value_route = request.POST['busroute']  
        route_selected_price = BusRoute.objects.get(title=selected_value_route)
        client.charge_ticket(route_selected_price)
        client.save()  

    context={
        'route' : route,
        'ticket' : ticket
    }
    return render(request,'main/index.html',context)

def register(request):
    if request.method == 'POST':
        form = ClientRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('index')

    else:
        form = ClientRegisterForm()

    return render(request, 'main/register.html', {'form': form})

def digital_wallet(request):
    client = request.user.client
    if request.method == 'POST':
        balance_to_add = float(request.POST['balance_to_add'])
        client.add_balance(balance_to_add)
        client.save()

    context = {
        'client' : client
    }
    return render(request,'main/digital_wallet.html', context)
