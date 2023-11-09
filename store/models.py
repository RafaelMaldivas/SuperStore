from django.db import models
from categoria.models import Categoria
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg
# Create your models here.
class Produto(models.Model):
    produto_nome = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    descricao = models.TextField(max_length=800, blank=True)
    preco = models.FloatField()
    foto = models.ImageField(upload_to='photos/produtos')
    estoque = models.IntegerField()
    avaliavel = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    criado_date = models.DateTimeField(auto_now_add=True)
    modificado_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'produto'
        verbose_name_plural  ='produtos'

    def get_url(self):
        return reverse('product_detail', args=[self.categoria.slug, self.slug])

    def __str__(self):
        return self.produto_nome
    
    def mediaReview(self):
        reviews = ReviewRating.objects.filter(produto=self, status=True)
        if reviews.count() > 0:
            return reviews.aggregate(average=Avg('rating'))['average']
        else:
            return 0
        
    def countReview(self):
        reviews = ReviewRating.objects.filter(produto=self, status=True)
        if reviews.count() > 0:
            return reviews.count()
        else:
            return 0

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_categoria='color', is_active=True)
    
    def sizes(self):
        return super(VariationManager, self).filter(variation_categoria='size', is_active=True)

variation_categoria_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    variation_categoria = models.CharField(max_length=100, choices=variation_categoria_choice)
    variation_valor = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def _str_(self):
        return self.variation_valor
    

class ReviewRating(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject