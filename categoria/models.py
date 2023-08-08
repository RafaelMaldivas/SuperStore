from django.db import models
from django.urls import reverse

# Create your models here.
class Categoria(models.Model):
    categoria_nome = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    descricao = models.TextField(max_length=500, blank=True)
    cat_imagem = models.ImageField(upload_to='photos/categorias', blank=True)

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural  ='categorias'

    
    def get_url(self):
        return reverse('produtos_por_categoria', args=[self.slug])


    def __str__(self):
        return self.categoria_nome