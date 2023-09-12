from django.shortcuts import render, redirect
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order
import mercadopago



sdk = mercadopago.SDK("APP_USR-4427427821291868-091015-077fa150887ef28ff5a3360d3ece1747-253859971")
# ...
'''payment_data = {
    "transaction_amount": 100,
    "token": "CARD_TOKEN",
    "description": "Payment description",
    "payment_method_id": 'visa',
    "installments": 1,
    "payer": {
        "email": 'test_user_123456@testuser.com'
    }
}
result = sdk.payment().create(payment_data)
payment = result["response"]

print(payment)'''

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

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

            context = {
                'order':order,
                'cart_items': cart_items,
                'total':total,
                'taxa':taxa,
                'grand_total':grand_total,

            }
            
            return render(request, 'orders/pagamento.html', context)
    else:
        return redirect('checkout')
            

def pagamento(request):
              
    return render(request, 'orders/pagamento.html')