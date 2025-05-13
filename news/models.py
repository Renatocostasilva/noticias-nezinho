from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.utils.text import slugify
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from PIL import Image
import uuid
import os
import time
import re

def get_file_path(instance, filename):
    """Generate a unique file path for uploaded images."""
    ext = filename.split('.')[-1].lower()
    if ext not in ['jpg', 'jpeg', 'png']:
        ext = 'jpg'
    filename = f"{uuid.uuid4()}.{ext}"
    return filename  # Salva diretamente na raiz de MEDIA_ROOT

def get_partner_image_path(instance, filename):
    """Gerar um caminho único para imagens de parceiros."""
    ext = filename.split('.')[-1]
    filename = f"{int(time.time())}.{ext}"
    return os.path.join('partner_images', filename)

def news_image_upload_path(instance, filename):
    """Caminho para salvar imagens de notícias usando apenas o nome original"""
    # Garantir que o nome do arquivo não tenha caracteres especiais
    
    # Extrair nome base e extensão
    name_parts = filename.split('.')
    if len(name_parts) > 1:
        extension = name_parts[-1].lower()
        # Verificar extensão
        if extension not in ['jpg', 'jpeg', 'png']:
            extension = 'jpg'
    else:
        extension = 'jpg'
    
    # Usar UUID para garantir nome único
    unique_id = uuid.uuid4().hex
    
    # Retornar caminho simples sem subdiretórios
    return f"news_images/{unique_id}.{extension}"

class Category(models.Model):
    """Model for news categories."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=20, default='#007bff')
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('news:category', kwargs={'slug': self.slug})
    
    def get_news_count(self):
        return self.news_set.filter(status='published').count()

class News(models.Model):
    """Model for news articles."""
    STATUS_CHOICES = (
        ('draft', 'Rascunho'),
        ('published', 'Publicado'),
    )
    
    title = models.CharField('Título', max_length=200)
    slug = models.SlugField('Slug', max_length=200, unique_for_date='publish_date')
    author = models.ForeignKey(User, verbose_name='Autor', on_delete=models.CASCADE, related_name='news_articles')
    content = RichTextUploadingField('Conteúdo')
    featured_image = models.ImageField(
        'Imagem Destacada',
        upload_to=news_image_upload_path,
        max_length=255
    )
    category = models.ForeignKey(Category, verbose_name='Categoria', on_delete=models.CASCADE)
    tags = TaggableManager('Tags')
    publish_date = models.DateTimeField('Data de Publicação', default=timezone.now)
    created_date = models.DateTimeField('Data de Criação', auto_now_add=True)
    updated_date = models.DateTimeField('Data de Atualização', auto_now=True)
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField('Em Destaque', default=False)
    is_slider = models.BooleanField('No Slider', default=False)
    is_trending = models.BooleanField('Em Tendência', default=False)
    summary = models.TextField('Resumo', max_length=500, blank=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')
    
    class Meta:
        verbose_name = 'Notícia'
        verbose_name_plural = 'Notícias'
        ordering = ['-publish_date']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Garantir que o slug seja criado a partir do título
        if not self.slug:
            self.slug = slugify(self.title)
            # Verificar se já existe outro objeto com o mesmo slug na mesma data
            counter = 1
            slug_original = self.slug
            while News.objects.filter(
                slug=self.slug,
                publish_date__year=self.publish_date.year,
                publish_date__month=self.publish_date.month,
                publish_date__day=self.publish_date.day
            ).exclude(pk=self.pk).exists():
                self.slug = f"{slug_original}-{counter}"
                counter += 1
        
        # Generate summary if not provided
        if not self.summary and self.content:
            # Strip HTML tags and limit to 300 characters
            from django.utils.html import strip_tags
            plain_content = strip_tags(self.content)
            self.summary = plain_content[:300] + '...' if len(plain_content) > 300 else plain_content
        
        super().save(*args, **kwargs)
        
        # Verificar se a imagem existe antes de tentar redimensioná-la
        try:
            if self.featured_image and hasattr(self.featured_image, 'path') and os.path.exists(self.featured_image.path):
                img = Image.open(self.featured_image.path)
                if img.height > 800 or img.width > 1200:
                    output_size = (1200, 800)
                    img.thumbnail(output_size)
                    img.save(self.featured_image.path)
        except Exception as e:
            print(f"Erro ao processar imagem: {e}")
            # Não bloqueia o salvamento se houver erro na imagem
    
    def get_absolute_url(self):
        return reverse('news:news_detail', kwargs={
            'year': self.publish_date.year,
            'month': self.publish_date.month,
            'day': self.publish_date.day,
            'slug': self.slug
        })
    
    def get_related_news(self):
        """Obter notícias relacionadas com base na categoria e tags."""
        return News.objects.filter(
            category=self.category, 
            status='published'
        ).exclude(id=self.id)[:4]

class Comment(models.Model):
    """Modelo para comentários de notícias."""
    news = models.ForeignKey(News, verbose_name='Notícia', on_delete=models.CASCADE, related_name='comments')
    name = models.CharField('Nome', max_length=100)
    email = models.EmailField('Email')
    content = models.TextField('Conteúdo')
    created_date = models.DateTimeField('Data de Criação', auto_now_add=True)
    active = models.BooleanField('Ativo', default=True)
    parent = models.ForeignKey('self', verbose_name='Comentário Pai', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['-created_date']
    
    def __str__(self):
        return f'Comentário de {self.name} em {self.news}'

class Newsletter(models.Model):
    """Modelo para inscrições na newsletter."""
    email = models.EmailField('Email', unique=True)
    subscribed_date = models.DateTimeField('Data de Inscrição', auto_now_add=True)
    active = models.BooleanField('Ativo', default=True)
    
    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'
    
    def __str__(self):
        return self.email

class Partner(models.Model):
    """Modelo para parceiros."""
    name = models.CharField('Nome', max_length=100)
    title = models.CharField('Título/Especialidade', max_length=100)
    description = RichTextUploadingField('Descrição')
    photo = models.ImageField('Foto', upload_to=get_partner_image_path)
    active = models.BooleanField('Ativo', default=True)
    order = models.PositiveIntegerField('Ordem', default=0)
    created_date = models.DateTimeField('Data de Criação', auto_now_add=True)
    updated_date = models.DateTimeField('Data de Atualização', auto_now=True)
    
    class Meta:
        verbose_name = 'Parceiro'
        verbose_name_plural = 'Parceiros'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Redimensionar a foto se necessário
        if self.photo:
            img = Image.open(self.photo.path)
            if img.height > 600 or img.width > 600:
                output_size = (600, 600)
                img.thumbnail(output_size)
                img.save(self.photo.path)

class ConsultationRequest(models.Model):
    """Modelo para solicitações de consulta com parceiros."""
    PAYMENT_CHOICES = (
        ('credit', 'Cartão de Crédito'),
        ('debit', 'Cartão de Débito'),
        ('pix', 'PIX'),
        ('bank_transfer', 'Transferência Bancária'),
        ('cash', 'Dinheiro'),
    )
    
    partner = models.ForeignKey(Partner, verbose_name='Parceiro', on_delete=models.CASCADE, related_name='consultation_requests')
    full_name = models.CharField('Nome Completo', max_length=200)
    cpf = models.CharField('CPF', max_length=14)
    email = models.EmailField('Email')
    phone = models.CharField('Telefone', max_length=20)
    address = models.TextField('Endereço')
    preferred_days = models.CharField('Dias Preferidos', max_length=200)
    preferred_times = models.CharField('Horários Preferidos', max_length=200)
    payment_method = models.CharField('Forma de Pagamento', max_length=20, choices=PAYMENT_CHOICES)
    notes = models.TextField('Observações', blank=True)
    created_date = models.DateTimeField('Data de Solicitação', auto_now_add=True)
    status = models.CharField('Status', max_length=20, default='pending', choices=(
        ('pending', 'Pendente'),
        ('confirmed', 'Confirmada'),
        ('cancelled', 'Cancelada'),
    ))
    
    class Meta:
        verbose_name = 'Solicitação de Consulta'
        verbose_name_plural = 'Solicitações de Consulta'
        ordering = ['-created_date']
    
    def __str__(self):
        return f'Consulta de {self.full_name} com {self.partner}'

class RSSFeed(models.Model):
    """Modelo para fontes de notícias RSS."""
    name = models.CharField('Nome', max_length=100)
    url = models.URLField('URL do Feed', max_length=255)
    active = models.BooleanField('Ativo', default=True)
    logo = models.ImageField('Logo', upload_to='rss_logos/', blank=True, null=True)
    category = models.ForeignKey(Category, verbose_name='Categoria', on_delete=models.SET_NULL, blank=True, null=True)
    order = models.PositiveIntegerField('Ordem', default=0)
    max_items = models.PositiveIntegerField('Máximo de Itens', default=5)
    created_date = models.DateTimeField('Data de Criação', auto_now_add=True)
    updated_date = models.DateTimeField('Data de Atualização', auto_now=True)
    
    class Meta:
        verbose_name = 'Feed RSS'
        verbose_name_plural = 'Feeds RSS'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name 