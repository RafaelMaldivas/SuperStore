from django.shortcuts import render
from store.models import Produto


def home(request):
    produto = Produto.objects.all().filter(avaliavel=True)

    context = {
        'produtos': produto,
    }
    return render(request, 'home.html', context)
