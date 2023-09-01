from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .forms import RegisterForms, Account
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# verificação de email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

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

            # ativação do usuário
            current_site = get_current_site(request)
            mail_subject = '[Do not reply] Por favor ative sua conta Super Store'
            message = render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            # messages.success(request, 'Obrigado por se cadastrar na SuperStore. Favor verificar seu email para ativar seu cadastro!')
            return redirect('/accounts/login/?command=verification&email=' + email)
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
            return redirect('dashboard')
        else:
            messages.error(request, 'Erro ao logar, verifique suas credenciais')
            return redirect('login')
        
    return render(request, 'accounts/login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Você saiu da sua conta')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Parabéns! Sua Conta está ativa!')
        return redirect('login')
    else:
        messages.error(request, 'Link de ativação inválido')
        return redirect('register')
    

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def forgotPassword(request):
    if request.method == 'POST': 
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # reset password email
            current_site = get_current_site(request)
            mail_subject = '[Do not reply] Reset seu Password'
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Foi enviado uma solicitação de renovação de nova senha para seu email')
            return redirect('login')

        else:
            messages.error(request, 'Conta Inexistente')
            return redirect('forgotPassword')
                    
    return render(request, 'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Por Favor reset a sua senha')
        return redirect('resetPassword')
    else:
        messages.error(request, 'Este Link foi expirado!')
        return redirect('login')
    


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,  'Sua Senha foi alterada com sucesso!!')
            return redirect('login')
        else:
            messages.error(request, 'As senhas não combinam!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')
