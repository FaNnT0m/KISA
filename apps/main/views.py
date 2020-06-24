from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ClientRegisterForm
from apps.main.models import District

def base(request):
    return render(request,'main/base.html')

def index(request):
    district = District.objects.values_list('name', flat=True) #Con 'flat' retorna el set limpio, sin comillas ni parentesis
    return render(request,'main/index.html',{'district':district})

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
