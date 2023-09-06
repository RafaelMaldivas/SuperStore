from django.db import models
from accounts.models import Account
from store.models import Produto, Variation


# Create your models here.
class Pagamento(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    pagamento_id = models.CharField(max_length=100)
    pagamento_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pagamento_id


class Order(models.Model):
    STATUS = (
        ("New", "New"),
        ("Accepted", "Accepted"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    pagamento = models.ForeignKey(
        Pagamento, on_delete=models.SET_NULL, blank=True, null=True
    )
    order_number = models.CharField(max_length=20)
    primeiro_nome = models.CharField(max_length=50)
    ultimo_nome = models.CharField(max_length=50)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    cep = models.CharField(max_length=8)
    endereco = models.CharField(max_length=50)
    numero = models.IntegerField()
    complemento = models.CharField(max_length=20)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    uf = models.CharField(max_length=2)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    taxa = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default="New")
    ip = models.CharField(max_length=20, blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.primeiro_nome


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pagamento = models.ForeignKey(
        Pagamento, on_delete=models.SET_NULL, blank=True, null=True
    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    quantidade = models.IntegerField()
    produto_preco = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.produto.produto_nome
