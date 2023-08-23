from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from store.models import Variation, Produto
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, produto_id):
    produto = Produto.objects.get(id=produto_id)  # pega o produto
    produto_variation = []
    if request.method == "POST":
        for item in request.POST:
            key = item
            value = request.POST[key]
            # print(key, value)

            try:
                variation = Variation.objects.get(
                    produto=produto,
                    variation_categoria__iexact=key,
                    variation_valor__iexact=value,
                )
                produto_variation.append(variation)
            except:
                pass

    try:
        cart = Cart.objects.get(
            cart_id=_cart_id(request)
        )  # pega o carrinho usando o cart_id presente na session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    try:
        cart_item = CartItem.objects.get(produto=produto, cart=cart)
        if len(produto_variation) > 0:
            cart_item.variations.clear()
            for item in produto_variation:
                cart_item.variations.add(item)
        cart_item.quantidade += 1  # cart_item adicona outro item
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            produto=produto,
            quantidade=1,
            cart=cart,
        )
        if len(produto_variation) > 0:
            cart_item.variations.clear()
            for item in produto_variation:
                cart_item.variations.add(item)
    cart_item.save()

    return redirect("cart")


def cart(request, total=0, quantidade=0, cart_items=None):
    try:
        taxa = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            quantidade += cart_item.quantidade
            total += cart_item.produto.preco * cart_item.quantidade
        if total < 500:
            taxa = (3 * total) / 100
        else:
            taxa = (2 * total) / 100
        grand_total = total + taxa

    except ObjectDoesNotExist:
        pass

    context = {
        "total": total,
        "quantidade": quantidade,
        "cart_items": cart_items,
        "taxa": taxa,
        "grand_total": grand_total,
    }
    return render(request, "store/cart.html", context)


def remove_cart(request, produto_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    produto = get_object_or_404(Produto, id=produto_id)
    cart_item = CartItem.objects.get(produto=produto, cart=cart)
    if cart_item.quantidade > 1:
        cart_item.quantidade -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect("cart")


def remove_cart_item(request, produto_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    produto = get_object_or_404(Produto, id=produto_id)
    cart_item = CartItem.objects.get(produto=produto, cart=cart)

    cart_item.delete()
    return redirect("cart")
