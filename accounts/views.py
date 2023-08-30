from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .forms import RegisterForms, Account
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForms(request.POST)
        if form.is_valid():
            primeiro_nome = form.cleaned_data['primeiro_nome']
            ultimo_nome = form.cleaned_data['ultimo_nome']
            email = form.cleaned_data['email']
            telefone = form.cleaned_data['telefone']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(primeiro_nome=primeiro_nome, ultimo_nome=ultimo_nome, email=email, username=username, password=password)    
            user.telefone = telefone
            user.save()
            messages.success(request, 'Registro efetuado com sucesso!')
            return redirect('register')
    else:
        form = RegisterForms()
   
    context = {
        'form':form,
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user  = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Você está logado!')
            return redirect('home')
        else:
            messages.error(request, 'Erro ao logar, verifique suas credenciais')
            return redirect('login')
        
    return render(request, 'accounts/login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Você saiu da sua conta')
    return redirect('login')