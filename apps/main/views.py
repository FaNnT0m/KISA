from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ClientRegisterForm,DistrictForm
from apps.main.models import *

# Son las vistas
def base(request):
    return render(request,'main/base.html')

def index(request):
    return render(request,'main/index.html')

def ticket_payment(request):
    district = District.objects.values_list('name', flat=True) #Con 'flat' retorna el set limpio, sin comillas ni parentesis
    route= BusRoute.objects.values_list('title',flat=True)
    ticket =BusRoute.objects.values_list('ticket_price',flat=True)
    formDis= DistrictForm()
    formDis.fields['province'].choices=((1,'San Jose'),)
    client = request.user.client

    if request.method == 'POST': # Se hace la consulta si es un Post sino
        selected_value_route = request.POST['busroute']  
        route_selected_price = BusRoute.objects.get(title=selected_value_route)
        client.charge_ticket(route_selected_price)#
        client.save()  # se guarda el cliente

    context={
        'district' : district,
        'formDis' : formDis,
        'route' : route,
        'ticket' : ticket
    }
    return render(request,'main/index.html',context)# Si no lo es, se renderiza

def register(request):# hace una solicitud de registro de nombre.
    if request.method == 'POST': # si se  cumple el motodo POST envie los datos 
        form = ClientRegisterForm(request.POST)
        if form.is_valid():# Si este es valido y cumple con los parametros
            form.save()# Aqui se guarda
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')# Se crea la cuenta
            return redirect('index')

    else:
        form = ClientRegisterForm() 

    return render(request, 'main/register.html', {'form': form})# Sino no se cumple, se redenriza

def digital_wallet(request):#muestra el #hace la solicitud de digital_wallet
    client = request.user.client # hace la solicitud para dar la respuesta 
    if request.method == 'POST':  # si se cumple el motodo POST envie los datos 
        balance_to_add = float(request.POST['balance_to_add'])# Agrega el balance de la cuenta y lo lleva hasta cuenta # Lo conviente de String a Float
        client.add_balance(balance_to_add)# agregua el monto al balance
        client.save()# guarde el monto

    context = {
        'client' : client# se envia el dinero al cliente
    }
    return render(request,'main/digital_wallet.html', context)
    


