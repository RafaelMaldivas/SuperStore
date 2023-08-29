from django import forms
from .models  import Account

class RegisterForms(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Crie uma senha',
        'class':'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirme sua senha'
    }))
    class Meta:
        model = Account
        fields = [
            'primeiro_nome', 'ultimo_nome', 'telefone', 'email', 'password'
        ]

    def clean(self):
        cleaned_data = super(RegisterForms, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "As senhas não combinam!!"
            )


    def __init__(self, *args, **kwargs):
        super(RegisterForms, self).__init__(*args, **kwargs)
        self.fields['primeiro_nome'].widget.attrs['placeholder'] = 'Digite o Primeiro Nome'
        self.fields['ultimo_nome'].widget.attrs['placeholder'] = 'Digite o Último Nome'
        self.fields['telefone'].widget.attrs['placeholder'] = 'Digite o número do celular'
        self.fields['email'].widget.attrs['placeholder'] = 'Digite o seu email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    
    