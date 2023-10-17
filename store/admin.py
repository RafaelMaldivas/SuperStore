from django.contrib import admin
from .models import Produto, Variation, ReviewRating

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('produto_nome',)}
    list_display = ('produto_nome', 'slug', 'preco', 'estoque',
                     'categoria', 'modificado_date', 'avaliavel')


class VariationAdmin(admin.ModelAdmin):
    list_display = ('produto', 'variation_categoria', 'variation_valor', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('produto', 'variation_categoria', 'variation_valor')

admin.site.register(Produto, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)