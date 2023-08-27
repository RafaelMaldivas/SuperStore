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

    is_cart_item_exists = CartItem.objects.filter(produto=produto, cart=cart).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(produto=produto, cart=cart)
        # se existir variações -> relacionado ao DB
        # considerar a variação corrente -> relacionado a lista de variações
        # considerar item_id -> relacionado ao DB
        ex_var_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)

        print(ex_var_list)

        if produto_variation in ex_var_list:
            # condiçao de incremento de product.variation no cart
            index = ex_var_list.index(produto_variation)
            item_id = id[index]
            item = CartItem.objects.get(produto=produto, id=item_id)
            item.quantidade += 1
            item.save()

        else:
            item = CartItem.objects.create(produto=produto, quantidade=1, cart=cart)
            # cria novo item no cart
            if len(produto_variation) > 0:
                item.variations.clear()
                item.variations.add(*produto_variation)
            item.save()
    else:
        cart_item = CartItem.objects.create(
            produto=produto,
            quantidade=1,
            cart=cart,
        )
        if len(produto_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*produto_variation)
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


def remove_cart(request, produto_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    produto = get_object_or_404(Produto, id=produto_id)
    try:     
        cart_item = CartItem.objects.get(produto=produto, cart=cart, id=cart_item_id)
        if cart_item.quantidade > 1:
            cart_item.quantidade -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect("cart")


def remove_cart_item(request, produto_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    produto = get_object_or_404(Produto, id=produto_id)
    cart_item = CartItem.objects.get(produto=produto, cart=cart, id=cart_item_id)

    cart_item.delete()
    return redirect("cart")
