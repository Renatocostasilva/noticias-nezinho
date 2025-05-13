from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin para o modelo UserProfile."""
    list_display = ('user', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('updated_at',)
    fieldsets = (
        ('Informações do Usuário', {
            'fields': ('user', 'profile_image', 'bio')
        }),
        ('Datas', {
            'fields': ('updated_at',)
        }),
    ) 