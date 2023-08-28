from django import forms
from .models  import Account

class RegisterForms(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            'primeiro_nome', 'ultimo_nome', 'telefone', 'email', 'password'
        ]