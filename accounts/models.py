from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

class UserProfile(models.Model):
    """Modelo para armazenar informações adicionais do usuário."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(
        upload_to='profile_images/',
        default='profile_images/default.png',
        verbose_name=_('Foto de Perfil')
    )
    bio = models.TextField(max_length=500, blank=True, verbose_name=_('Biografia'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))

    class Meta:
        verbose_name = _('Perfil de Usuário')
        verbose_name_plural = _('Perfis de Usuários')

    def __str__(self):
        return f'Perfil de {self.user.username}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Cria um perfil de usuário automaticamente quando um novo usuário é criado."""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Salva o perfil do usuário quando o usuário é salvo."""
    instance.profile.save() 