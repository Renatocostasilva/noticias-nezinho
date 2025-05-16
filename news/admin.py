from django.contrib import admin
from .models import Category, News, Comment, Newsletter, SiteConfiguration

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publish_date', 'status', 'is_featured', 'is_slider')
    list_filter = ('status', 'category', 'is_featured', 'is_slider', 'is_trending', 'publish_date')
    search_fields = ('title', 'content', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish_date'
    ordering = ('-publish_date',)
    list_editable = ('status', 'is_featured', 'is_slider')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'category', 'featured_image', 'content')
        }),
        ('Options', {
            'fields': ('summary', 'tags', 'status', 'publish_date')
        }),
        ('Featured Options', {
            'fields': ('is_featured', 'is_slider', 'is_trending'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'news', 'created_date', 'active')
    list_filter = ('active', 'created_date')
    search_fields = ('name', 'email', 'content')
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    approve_comments.short_description = "Approve selected comments"
    
    def disapprove_comments(self, request, queryset):
        queryset.update(active=False)
    disapprove_comments.short_description = "Disapprove selected comments"

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_date', 'active')
    list_filter = ('active', 'subscribed_date')
    search_fields = ('email',)
    actions = ['activate_subscriptions', 'deactivate_subscriptions']
    
    def activate_subscriptions(self, request, queryset):
        queryset.update(active=True)
    activate_subscriptions.short_description = "Activate selected subscriptions"
    
    def deactivate_subscriptions(self, request, queryset):
        queryset.update(active=False)
    deactivate_subscriptions.short_description = "Deactivate selected subscriptions"

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'updated_at']
    fieldsets = (
        ('Informações do Site', {
            'fields': ('site_name', 'site_logo')
        }),
        ('Rodapé', {
            'fields': ('footer_text',)
        }),
    )

    def has_add_permission(self, request):
        # Impede que novos registros sejam criados se já existir um
        return not SiteConfiguration.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Impede que o registro único seja excluído
        return False 