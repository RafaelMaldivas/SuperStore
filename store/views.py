from django.shortcuts import render, get_object_or_404
from .models import Produto
from categoria.models import Categoria

# Create your views here.


def store(request, categoria_slug=None):
    categorias = None
    produto = None
    if categoria_slug != None:
        categorias = get_object_or_404(Categoria, slug=categoria_slug)
        produto = Produto.objects.filter(categoria=categorias, avaliavel=True)
        produto_count = produto.count()
    else:
        produto = Produto.objects.all().filter(avaliavel=True)
        produto_count = produto.count()
    context = {
        'produtos': produto,
        'produto_count' : produto_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, categoria_slug, produto_slug):
    try:
        single_product = Produto.objects.get(categoria__slug=categoria_slug, slug=produto_slug)
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
    }

    return render(request, 'store/product_detail.html', context)
