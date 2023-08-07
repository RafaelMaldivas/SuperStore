from django.contrib import admin
from .models import Produto

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('produto_nome',)}
    list_display = ('produto_nome', 'slug', 'preco', 'estoque',
                     'categoria', 'modificado_date', 'avaliavel')


admin.site.register(Produto, ProductAdmin)