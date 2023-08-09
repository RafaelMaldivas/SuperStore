from django.shortcuts import render, get_object_or_404
from .models import Produto, Categoria
import random
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


