from django.contrib import admin
from .models import Pagamento, Order, OrderProduct
# Register your models here.

admin.site.register(Pagamento)
admin.site.register(Order)
admin.site.register(OrderProduct)


