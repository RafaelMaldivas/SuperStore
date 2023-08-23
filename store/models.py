from django.db import models
from categoria.models import Categoria
from django.urls import reverse
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