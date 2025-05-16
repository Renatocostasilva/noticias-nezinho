from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import FileExtensionValidator

class Photo(models.Model):
    """Modelo para armazenar fotos dos anúncios"""
    image = models.ImageField(upload_to='classifieds/photos/%Y/%m/%d/', 
                             validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Foto {self.id}"

class Ad(models.Model):
    """Modelo para anúncios de classificados"""
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
    )
    
    title = models.CharField('Título', max_length=100)
    description = models.TextField('Descrição', max_length=10000)
    photos = models.ManyToManyField(Photo, blank=True)
    
    # Dados pessoais (confidenciais)
    name = models.CharField('Nome', max_length=100)
    email = models.EmailField('Email')
    phone = models.CharField('Telefone', max_length=20)
    
    # Campos de controle
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='pending')
    highlight = models.BooleanField('Destacado', default=False)
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    updated_at = models.DateTimeField('Data de Atualização', auto_now=True)
    
    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        ordering = ['-highlight', '-created_at']
    
    def __str__(self):
        return self.title
        
    def photo_count(self):
        return self.photos.count()
    photo_count.short_description = 'Número de fotos'

class ContactMessage(models.Model):
    """Modelo para mensagens de contato entre usuários e anunciantes"""
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='messages')
    sender_name = models.CharField('Nome', max_length=100)
    sender_email = models.EmailField('Email')
    message = models.TextField('Mensagem')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Mensagem de Contato'
        verbose_name_plural = 'Mensagens de Contato'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Mensagem de {self.sender_name} para {self.ad.title}"
