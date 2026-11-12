from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['endereco', 'telefone']
        widgets = {
            'endereco': forms.Textarea(attrs={
                'class': 'form-input', 
                'rows': 3, 
                'placeholder': 'Rua Exemplo, 123...'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-input', 
                'placeholder': '(00) 90000-0000'
            }),
        }
        labels = {
            'endereco': 'Endereço de Entrega',
            'telefone': 'WhatsApp para contato',
        }