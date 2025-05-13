from django import forms
from .models import Ad, ContactMessage, Photo

class AdForm(forms.ModelForm):
    """Formulário para submissão de anúncios"""
    photos = forms.ImageField(
        label='Fotos (máximo 5)',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    
    highlight = forms.BooleanField(
        label='Destacar anúncio (R$ 10,00)',
        required=False
    )
    
    class Meta:
        model = Ad
        fields = ['title', 'description', 'name', 'email', 'phone', 'highlight']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'maxlength': 200, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ContactForm(forms.ModelForm):
    """Formulário para contato com anunciantes"""
    class Meta:
        model = ContactMessage
        fields = ['sender_name', 'sender_email', 'message']
        widgets = {
            'sender_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sender_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

class PaymentForm(forms.Form):
    """Formulário simulado de pagamento"""
    card_number = forms.CharField(
        label='Número do Cartão', 
        max_length=16,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    card_name = forms.CharField(
        label='Nome no Cartão', 
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    expiry_date = forms.CharField(
        label='Data de Validade', 
        max_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/AA'})
    )
    cvv = forms.CharField(
        label='CVV', 
        max_length=3,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    ) 