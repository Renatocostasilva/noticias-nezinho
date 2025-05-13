from django import forms
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import News, Category, Comment, Newsletter, Partner, ConsultationRequest, RSSFeed
import re

class NewsForm(forms.ModelForm):
    """Form for creating and updating news articles."""
    content = forms.CharField(widget=CKEditorUploadingWidget())
    featured_image = forms.ImageField(
        label='Imagem Destacada',
        required=False,
        error_messages={
            'invalid_image': 'O arquivo enviado não é uma imagem válida.'
        },
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/jpeg,image/png,image/jpg'
        })
    )
    
    # Tornar o campo slug opcional
    slug = forms.SlugField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o slug (opcional)'
        }),
        help_text='Nome amigável para URL. Deixe em branco para gerar automaticamente a partir do título.'
    )
    
    class Meta:
        model = News
        fields = [
            'title', 'slug', 'category', 'featured_image', 'content', 
            'summary', 'tags', 'status', 'is_featured', 
            'is_slider', 'is_trending', 'publish_date'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o título'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o slug (opcional)'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Digite um breve resumo (opcional)'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite as tags separadas por vírgulas'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'publish_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_slider': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_trending': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'slug': _('Nome amigável para URL. Deixe em branco para gerar automaticamente a partir do título.'),
            'tags': _('Digite as tags separadas por vírgulas.'),
            'is_featured': _('Notícias em destaque aparecem na página inicial.'),
            'is_slider': _('Notícias do slider aparecem no slider principal.'),
            'is_trending': _('Notícias em tendência aparecem na seção de tendências.'),
        }
        labels = {
            'title': _('Título'),
            'slug': _('Slug'),
            'category': _('Categoria'),
            'featured_image': _('Imagem Destacada'),
            'content': _('Conteúdo'),
            'summary': _('Resumo'),
            'tags': _('Tags'),
            'status': _('Status'),
            'publish_date': _('Data de Publicação'),
            'is_featured': _('Em Destaque'),
            'is_slider': _('No Slider'),
            'is_trending': _('Em Tendência'),
        }

    def clean_featured_image(self):
        """Validação simples para o campo de imagem."""
        image = self.cleaned_data.get('featured_image')
        if not image:
            return None
        
        # Log para depuração
        print(f"Validando imagem: {image.name} ({image.size} bytes)")
        
        # Verificar extensão
        valid_extensions = ['jpg', 'jpeg', 'png']
        ext = image.name.split('.')[-1].lower()
        if ext not in valid_extensions:
            raise forms.ValidationError("Formato de arquivo não suportado. Use JPG ou PNG.")
        
        # Verificar tamanho
        if image.size > 5 * 1024 * 1024:  # 5 MB
            raise forms.ValidationError("A imagem deve ter no máximo 5 MB.")
        
        return image

class CategoryForm(forms.ModelForm):
    """Form for creating and updating categories."""
    class Meta:
        model = Category
        fields = ['name', 'description', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome da categoria'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Digite a descrição da categoria'}),
            'color': forms.TextInput(attrs={'class': 'form-control color-picker', 'placeholder': 'Selecione a cor'}),
        }
        labels = {
            'name': _('Nome'),
            'description': _('Descrição'),
            'color': _('Cor'),
        }

class CommentForm(forms.ModelForm):
    """Form for creating comments."""
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu Nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Seu Email'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Seu Comentário'}),
        }
        labels = {
            'name': _('Nome'),
            'email': _('Email'),
            'content': _('Comentário'),
        }

class NewsletterForm(forms.ModelForm):
    """Form for newsletter subscriptions."""
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu email'}),
        }
        labels = {
            'email': '',
        }

class SearchForm(forms.Form):
    """Form for searching news."""
    q = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pesquisar...'}),
        required=False
    )

class PartnerForm(forms.ModelForm):
    """Formulário para criar e atualizar parceiros."""
    description = forms.CharField(widget=CKEditorUploadingWidget())
    
    class Meta:
        model = Partner
        fields = ['name', 'title', 'description', 'photo', 'active', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do parceiro'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título ou especialidade'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': _('Nome'),
            'title': _('Título/Especialidade'),
            'description': _('Descrição'),
            'photo': _('Foto'),
            'active': _('Ativo'),
            'order': _('Ordem de exibição'),
        }
        help_texts = {
            'order': _('Parceiros com menor número aparecem primeiro.'),
        }

def validate_cpf(cpf):
    """Validar CPF."""
    # Remove caracteres não numéricos
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Calcula o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    # Verifica o primeiro dígito verificador
    if digito1 != int(cpf[9]):
        return False
    
    # Calcula o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    # Verifica o segundo dígito verificador
    if digito2 != int(cpf[10]):
        return False
    
    return True

class ConsultationRequestForm(forms.ModelForm):
    """Formulário para solicitações de consulta."""
    class Meta:
        model = ConsultationRequest
        fields = [
            'partner', 'full_name', 'cpf', 'email', 'phone', 
            'address', 'preferred_days', 'preferred_times', 
            'payment_method', 'notes'
        ]
        widgets = {
            'partner': forms.Select(attrs={'class': 'form-select'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome completo'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu.email@exemplo.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Seu endereço completo'}),
            'preferred_days': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Segunda, Quarta e Sexta'}),
            'preferred_times': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Manhã ou após as 18h'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observações adicionais (opcional)'}),
        }
        labels = {
            'partner': _('Parceiro'),
            'full_name': _('Nome Completo'),
            'cpf': _('CPF'),
            'email': _('Email'),
            'phone': _('Telefone'),
            'address': _('Endereço'),
            'preferred_days': _('Dias Preferidos'),
            'preferred_times': _('Horários Preferidos'),
            'payment_method': _('Forma de Pagamento'),
            'notes': _('Observações'),
        }
    
    def clean_cpf(self):
        """Validar o CPF."""
        cpf = self.cleaned_data.get('cpf')
        if not validate_cpf(cpf):
            raise forms.ValidationError('CPF inválido. Por favor, verifique os números informados.')
        return cpf 

class RSSFeedForm(forms.ModelForm):
    """Formulário para gerenciar fontes de notícias RSS."""
    class Meta:
        model = RSSFeed
        fields = ['name', 'url', 'active', 'logo', 'category', 'order', 'max_items']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da fonte (Ex: Estadão, G1, etc.)'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://exemplo.com/feed.xml'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'max_items': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '20'}),
        }
        labels = {
            'name': _('Nome'),
            'url': _('URL do Feed'),
            'active': _('Ativo'),
            'logo': _('Logo'),
            'category': _('Categoria'),
            'order': _('Ordem de exibição'),
            'max_items': _('Máximo de Itens'),
        }
        help_texts = {
            'url': _('URL completa do feed RSS (normalmente termina com .xml, .rss ou /feed)'),
            'order': _('Feeds com menor número aparecem primeiro.'),
            'max_items': _('Número máximo de notícias a exibir deste feed (1-20)'),
        } 