from django.shortcuts import render
from .models import Produto
# Create your views here.

def store(request):
    produto = Produto.objects.all().filter(avaliavel=True)
    produto_count = produto.count()
    context = {
        'produtos': produto,
        'produto_count' : produto_count,
    }
    return render(request, 'store/store.html', context)
