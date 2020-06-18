from django.shortcuts import render
from .forms import UserForm, PersonForm
# Create your views here.
def home (request):
    return render(request,'main/index.html')

def register (request):
    user_form = UserForm(request.POST or None)
    person_form = PersonForm(request.POST or None)

    if user_form.is_valid() and person_form.is_valid():
        user_form.save()
        person_form.save()  
    
    context = {'user_form' : user_form, 'person_form' : person_form} # Two forms that will become one
    return render(request,'main/register.html', context)
