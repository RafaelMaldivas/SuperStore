from django.shortcuts import render, redirect
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order


# Create your views here.


def place_order(request, total=0, quantidade=0):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    taxa = 0
    
    for cart_item in cart_items:
        total += cart_item.produto.preco * cart_item.quantidade
        quantidade += cart_item.quantidade

    if total < 500:
        taxa = (3 * total) / 100
    else:
        taxa = (2 * total) / 100

    grand_total = total + taxa
     
    if request.method == 'POST':
        form = OrderForm(request.POST) 
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.primeiro_nome = form.cleaned_data['primeiro_nome']
            data.ultimo_nome = form.cleaned_data['ultimo_nome']
            data.telefone = form.cleaned_data['telefone']
            data.email = form.cleaned_data['email']                                                                         
            data.cep = form.cleaned_data['cep']
            data.logradouro = form.cleaned_data['logradouro']
            data.numero = form.cleaned_data['numero']
            data.complemento = form.cleaned_data['complemento']
            data.bairro = form.cleaned_data['bairro']
            data.cidade = form.cleaned_data['cidade']
            data.uf = form.cleaned_data['uf']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.taxa = taxa
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # gera o numero da ordem
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%d%m%Y") #06092023
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            return redirect('checkout')
    else:
        return redirect('checkout')
            
