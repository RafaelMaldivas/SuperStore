from django.shortcuts import render, redirect
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, OrderProduct, Pagamento
import mercadopago

from IPython.display import Image, display

import qrcode
from django.http import HttpResponse
from io import BytesIO


# Create your views here.
def place_order(request, total=0, quantidade=0):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect("store")

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

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.primeiro_nome = form.cleaned_data["primeiro_nome"]
            data.ultimo_nome = form.cleaned_data["ultimo_nome"]
            data.telefone = form.cleaned_data["telefone"]
            data.email = form.cleaned_data["email"]
            data.cep = form.cleaned_data["cep"]
            data.logradouro = form.cleaned_data["logradouro"]
            data.numero = form.cleaned_data["numero"]
            data.complemento = form.cleaned_data["complemento"]
            data.bairro = form.cleaned_data["bairro"]
            data.cidade = form.cleaned_data["cidade"]
            data.uf = form.cleaned_data["uf"]
            data.order_note = form.cleaned_data["order_note"]
            data.order_total = round(grand_total,2)
            data.taxa = round(taxa,2)
            data.ip = request.META.get("REMOTE_ADDR")
            data.save()

            # gera o numero da ordem
            yr = int(datetime.date.today().strftime("%Y"))
            dt = int(datetime.date.today().strftime("%d"))
            mt = int(datetime.date.today().strftime("%m"))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%d%m%Y")  # 06092023
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number
            )

            context = {
                "order": order,
                "cart_items": cart_items,
                "total": total,
                "taxa": taxa,
                "grand_total": grand_total,
            }

            return render(request, "orders/pagamento.html", context)
    else:
        return redirect("checkout")


def pagamento(request):
    mt = int(datetime.date.today().strftime("%m"))
    yr = int(datetime.date.today().strftime("%Y"))
    dt = int(datetime.date.today().strftime("%d"))
    d = datetime.date(dt, mt, yr)
    current_date = d.strftime("%Y%m%d")  # 06092023
    order_number = current_date + str(order_number.id)
    order_number.order_number = order_number

    order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)

    mt = int(datetime.date.today().strftime("%m"))
    yr = int(datetime.date.today().strftime("%Y"))
    d = datetime.date(mt, yr)
    current_date = d.strftime("%Y%m%d")  # 06092023
    pagamento_id = current_date + str(pagamento_id.id)
    pagamento_id.pagamento_id = pagamento_id

    pagamento = Pagamento(
        user = request.user,
        pagamento_id = pagamento_id,
        pagamento_method = "Pix",
        total_pago = order.order_total,
        status = "New",  
    )
    pagamento.save()

    order.pagamento = pagamento
    order.is_ordered = False
    order.save()

   
    # gera o numero da order_id      
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.pagamento = pagamento
        orderproduct.user_id = request.user.id
        orderproduct.produto_id = item.produto_id
        orderproduct.quantidade = item.quantidade
        orderproduct.variations = item.variations
        orderproduct.produto_preco = item.produto.preco
        orderproduct.ordered = True
        orderproduct.save()
    
    return render(request, "orders/pagamento.html")



def gerar_qrcode(request):
    email = request.GET.get("email", None)
    amount = request.GET.get("amount", None)
    if email:
        sdk = mercadopago.SDK(
            "APP_USR-4427427821291868-091015-077fa150887ef28ff5a3360d3ece1747-253859971"
        )
        payment_data = {
            "transaction_amount": float(amount.replace(",", ".")),
            "description": f"Super Store - {email}",
            "payment_method_id": "pix",
            "payer": {
                "email": request.GET.get("email", None),
                
            },
        }

        payment_response = sdk.payment().create(payment_data)
        payment = payment_response["response"]

        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=4,
        ) 
        
        # Adicione os dados ao QR code
        qr.add_data(payment["point_of_interaction"]["transaction_data"]["qr_code"])
        qr.make(fit=True)

        # Crie uma imagem do QR code usando a biblioteca PIL
        img = qr.make_image(fill_color="black", back_color="white")

        # Salve a imagem em um objeto BytesIO
        

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        image_data = buffer.getvalue()
        buffer.close()

        # Retorne a imagem como resposta HTTP
        return HttpResponse(image_data, content_type="image/png")

    else:
        return HttpResponse("Email não fornecido na URL.")
