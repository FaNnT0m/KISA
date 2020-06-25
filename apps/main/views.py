from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ClientRegisterForm
from .forms import District
from apps.main.models import District

def base(request):
    return render(request,'main/base.html')

def index(request):
    district = District.objects.values_list('name', flat=True) #Con 'flat' retorna el set limpio, sin comillas ni parentesis
    form = District.objects.values_list('province')
    return render(request,'main/index.html',{'district':district,'form':form})

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
