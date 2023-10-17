from django.shortcuts import render, get_object_or_404, redirect
from .models import Produto, ReviewRating
from categoria.models import Categoria
from carts.models import CartItem
from carts.views import _cart_id
from .forms import ReviewForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
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


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            produtos = Produto.objects.order_by('-criado_date').filter(Q(descricao__icontains=keyword) | Q(produto_nome__icontains=keyword))
            produto_count = produtos.count()
    context = {
        'produtos' : produtos,
        'produto_count': produto_count,
    }   
    return render(request, 'store/store.html', context)

def submit_review(request, produto_id):
    if request.method == 'POST':
        url = request.META.get('HTTP_REFERER')
        try:
            reviews = ReviewRating.objects.get(usuario__id=request.user.id, produto__id=produto_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Obrigado! Sua avaliação foi atualizada.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.produto_id = produto_id
                data.usuario_id = request.user.id
                data.save()
                messages.success(request, 'Obrigado! Sua avaliação foi enviada.')
                return redirect(url)
           
