from django.db import models
from categoria.models import Categoria
# Create your models here.
class Produto(models.Model):
    produto_nome = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    descricao = models.TextField(max_length=500, blank=True)
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

    def __str__(self):
        return self.produto_nome