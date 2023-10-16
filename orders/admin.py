from django.contrib import admin
from .models import Pagamento, Order, OrderProduct
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_number","primeiro_nome", "ultimo_nome", "telefone", "email", "cep", "logradouro", "numero", "complemento", "bairro", "cidade", "uf", "order_total", "taxa", "is_ordered"]
    list_filter = ["is_ordered"]
    search_fields = ["order_number","primeiro_nome", "ultimo_nome", "telefone", "email"]
    list_per_page = 20

admin.site.register(Pagamento)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)


