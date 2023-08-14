from django.shortcuts import render, get_object_or_404
from .models import Produto
from categoria.models import Categoria
from carts.models import CartItem
from carts.views import _cart_id
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.


def store(request, categoria_slug=None):
    categorias = None
    produto = None
    if categoria_slug != None:
        categorias = get_object_or_404(Categoria, slug=categoria_slug)
        produto = Produto.objects.filter(categoria=categorias, avaliavel=True)
        paginator = Paginator(produto, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        produto_count = produto.count()
    else:
        produto = Produto.objects.all().filter(avaliavel=True).order_by('id')
        paginator = Paginator(produto, 9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        produto_count = produto.count()
    context = {
        'produtos': paged_products,
        'produto_count' : produto_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, categoria_slug, produto_slug):
    try:
        single_product = Produto.objects.get(categoria__slug=categoria_slug, slug=produto_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), produto=single_product).exists()
        
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart':in_cart,
    }

    return render(request, 'store/product_detail.html', context)
