from django.db import models
from store.models import Produto, Variation
# Create your models here.
class Cart(models.Model):

    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    

class CartItem(models.Model):

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.produto.preco * self.quantidade
    
    def __unicode__(self):
        return self.produto