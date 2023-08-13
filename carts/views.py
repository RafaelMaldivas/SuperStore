from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, Cart, CartItem

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, produto_id):
    produto = Produto.objects.get(id=produto_id) #pega o produto
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # pega o carrinho usando o cart_id presente na session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(produto=produto, cart=cart)
        cart_item.quantidade += 1 # cart_item adicona outro item
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            produto = produto,
            quantidade = 1,
            cart = cart,
        )
    cart_item.save()
   
    return redirect('cart')

def cart(request, total=0, quantidade=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            quantidade += cart_item.quantidade
            total += (cart_item.produto.preco * cart_item.quantidade)
        if total < 500:
            taxa = (3 * total)/100
        else:
            taxa = (2 * total)/100
        grand_total = total + taxa

    except cart.ObjectNotExist:
        pass
    
    context = {
        'total':total,
        'quantidade':quantidade,
        'cart_items':cart_items,
        'taxa': taxa,
        'grand_total':grand_total,
    }
    return render(request, 'store/cart.html', context)

def remove_cart(request, produto_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    produto = get_object_or_404(Produto, id=produto_id)
    cart_item = CartItem.objects.get(produto=produto, cart=cart)
    if cart_item.quantidade > 1:
        cart_item.quantidade -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, produto_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    produto = get_object_or_404(Produto, id=produto_id)
    cart_item = CartItem.objects.get(produto=produto, cart=cart)

    cart_item.delete()
    return redirect('cart')