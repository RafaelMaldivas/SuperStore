from django.shortcuts import render
from .forms import RegisterForms

# Create your views here.
def register(request):
    form = RegisterForms()
    context = {
        'form':form,
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    return render(request, 'accounts/logout.html')