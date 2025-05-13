from django.contrib import admin
from .models import Ad, Photo, ContactMessage

class PhotoInline(admin.TabularInline):
    model = Ad.photos.through
    extra = 0

class ContactMessageInline(admin.TabularInline):
    model = ContactMessage
    extra = 0
    readonly_fields = ['sender_name', 'sender_email', 'message', 'created_at']
    can_delete = False

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'highlight', 'created_at', 'photo_count']
    list_filter = ['status', 'highlight', 'created_at']
    search_fields = ['title', 'description', 'name', 'email']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [PhotoInline, ContactMessageInline]
    exclude = ['photos']
    
    actions = ['approve_ads', 'reject_ads']
    
    def approve_ads(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f'{queryset.count()} anúncios foram aprovados.')
    approve_ads.short_description = 'Aprovar anúncios selecionados'
    
    def reject_ads(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f'{queryset.count()} anúncios foram rejeitados.')
    reject_ads.short_description = 'Rejeitar anúncios selecionados'

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'uploaded_at']
    readonly_fields = ['uploaded_at']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['sender_name', 'ad', 'created_at']
    list_filter = ['created_at']
    search_fields = ['sender_name', 'sender_email', 'message']
    readonly_fields = ['created_at']
