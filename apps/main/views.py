from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ClientRegisterForm,DistrictForm
from apps.main.models import *


def base(request):
    return render(request,'main/base.html')

def index(request):
    district = District.objects.values_list('name', flat=True) #Con 'flat' retorna el set limpio, sin comillas ni parentesis
    formDis= DistrictForm()
    formDis.fields['province'].choices=((1,'San Jose'),)
    client= Client.objects.get(pk=2)      #Aqui se utilizara una verificion de cual persona esta en el sistema para cobrarle
    
    route= BusRoute.objects.values_list('title',flat=True)
    context={'district':district,'formDis':formDis,'route':route}

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
