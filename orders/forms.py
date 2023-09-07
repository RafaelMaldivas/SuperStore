from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['primeiro_nome', 'ultimo_nome', 'telefone', 'email', 
                  'cep', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'uf', 'order_note' ]