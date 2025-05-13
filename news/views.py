from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy, reverse
from django.db.models import Count, Q, Sum
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from hitcount.views import HitCountDetailView
import feedparser
from datetime import datetime, timedelta
import time
from .models import News, Category, Comment, Newsletter, Partner, ConsultationRequest, RSSFeed
from .forms import NewsForm, CommentForm, NewsletterForm, SearchForm, PartnerForm, ConsultationRequestForm, RSSFeedForm
from classifieds.models import Ad  # Importar o modelo de anúncios
import random
from django.core.cache import cache

class HomeView(ListView):
    """View for the homepage."""
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news_list'
    paginate_by = 5
    
    def get_queryset(self):
        return News.objects.filter(status='published').select_related('author', 'category').order_by('-publish_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Slider news
        context['slider_news'] = News.objects.filter(status='published', is_slider=True).order_by('-publish_date')[:5]
        
        # Notícias em destaque
        context['featured_news'] = News.objects.filter(status='published', is_featured=True).order_by('-publish_date')[:3]
        
        # Notícias populares
        context['trending_news'] = News.objects.filter(status='published').order_by('-hit_count_generic__hits')[:5]
        
        # Estatísticas
        context['total_news'] = News.objects.filter(status='published').count()
        context['recent_comments'] = Comment.objects.select_related('news').order_by('-created_date')[:5]
        
        # Parceiros para o widget lateral
        context['partners'] = Partner.objects.filter(active=True).order_by('?')[:4]
        
        # Categorias para o widget lateral
        context['categories'] = Category.objects.all()
        
        # Anúncios em destaque
        context['featured_ads'] = Ad.objects.filter(
            status='approved', highlight=True
        ).order_by('-created_at')[:4]
        
        # Feeds RSS ativos
        context['active_feeds'] = RSSFeed.objects.filter(active=True).order_by('order')
        
        # Adicionar notícias de feeds RSS
        context['rss_feeds'] = self.get_rss_feeds()
        
        return context
    
    def get_rss_feeds(self):
        """Obter notícias de feeds RSS ativos."""
        # Verificar se os feeds estão em cache
        cached_feeds = cache.get('rss_feeds_cache')
        if cached_feeds:
            return cached_feeds
            
        # Se não estiverem em cache, buscar e processar normalmente
        active_feeds = RSSFeed.objects.filter(active=True).order_by('order')
        all_feed_entries = []
        
        for feed in active_feeds:
            try:
                feed_data = feedparser.parse(feed.url)
                
                if not feed_data.entries:
                    continue
                
                entries = []
                for entry in feed_data.entries[:feed.max_items]:
                    # Tentar extrair a imagem do feed
                    image_url = None
                    if 'media_content' in entry and entry.media_content:
                        for media in entry.media_content:
                            if 'url' in media:
                                image_url = media['url']
                                break
                    
                    # Tentar extrair de enclosures
                    if not image_url and 'enclosures' in entry and entry.enclosures:
                        for enclosure in entry.enclosures:
                            if 'url' in enclosure and enclosure.type and enclosure.type.startswith('image'):
                                image_url = enclosure.url
                                break
                    
                    # Tente extrair links de imagens do conteúdo usando expressões regulares
                    if not image_url and 'description' in entry:
                        import re
                        img_pattern = re.compile(r'<img[^>]+src="([^">]+)"')
                        match = img_pattern.search(entry.description)
                        if match:
                            image_url = match.group(1)
                    
                    # Formatar a data de publicação, se disponível
                    pub_date = None
                    if 'published_parsed' in entry and entry.published_parsed:
                        pub_date = time.strftime('%Y-%m-%d', entry.published_parsed)
                    elif 'updated_parsed' in entry and entry.updated_parsed:
                        pub_date = time.strftime('%Y-%m-%d', entry.updated_parsed)
                    
                    # Preparar o sumário
                    summary = ''
                    if 'summary' in entry:
                        summary = entry.summary
                    elif 'description' in entry:
                        summary = entry.description
                    
                    entry_data = {
                        'title': entry.title,
                        'link': entry.link,
                        'published': entry.get('published', ''),
                        'pub_date': pub_date,
                        'summary': summary,
                        'image_url': image_url,
                        'source': feed.name,
                        'source_url': feed.url,
                        'category': feed.category.name if feed.category else ''
                    }
                    entries.append(entry_data)
                
                if entries:
                    feed_info = {
                        'id': feed.id,
                        'name': feed.name,
                        'logo': feed.logo if feed.logo else None,
                        'entries': entries,
                        'category': feed.category.name if feed.category else 'Geral'
                    }
                    all_feed_entries.append(feed_info)
            except Exception as e:
                print(f"Erro ao processar feed {feed.name}: {str(e)}")
        
        # Armazenar em cache para futuras requisições
        if all_feed_entries:
            cache.set('rss_feeds_cache', all_feed_entries, 3600)  # Cache por 1 hora
            
        return all_feed_entries

class NewsDetailView(HitCountDetailView):
    """View for individual news articles."""
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    count_hit = True
    
    def get_object(self):
        return get_object_or_404(
            News,
            slug=self.kwargs['slug'],
            publish_date__year=self.kwargs['year'],
            publish_date__month=self.kwargs['month'],
            publish_date__day=self.kwargs['day'],
            status='published'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_news'] = self.object.get_related_news()
        context['comments'] = self.object.comments.filter(active=True, parent=None)
        context['comment_form'] = CommentForm()
        context['search_form'] = SearchForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = self.object
            
            # Check if it's a reply to another comment
            parent_id = request.POST.get('parent_id')
            if parent_id:
                new_comment.parent = get_object_or_404(Comment, id=parent_id)
            
            new_comment.save()
            messages.success(request, 'Your comment has been added successfully!')
            return redirect(self.object.get_absolute_url())
        
        context = self.get_context_data(object=self.object)
        context['comment_form'] = comment_form
        return self.render_to_response(context)

class CategoryNewsView(ListView):
    """View for news filtered by category."""
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news_list'
    paginate_by = 10
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return News.objects.filter(
            category=self.category,
            status='published'
        ).order_by('-publish_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['search_form'] = SearchForm()
        context['categories'] = Category.objects.all()
        # Adicionar parceiros ativos para exibição na barra lateral
        context['partners'] = Partner.objects.filter(active=True).order_by('order')[:2]
        return context

class SearchResultsView(ListView):
    """View for search results."""
    model = News
    template_name = 'news/search_results.html'
    context_object_name = 'news_list'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return News.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) |
                Q(summary__icontains=query),
                status='published'
            ).order_by('-publish_date')
        return News.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['search_form'] = SearchForm(initial={'q': context['query']})
        context['categories'] = Category.objects.all()
        # Adicionar parceiros ativos para exibição na barra lateral
        context['partners'] = Partner.objects.filter(active=True).order_by('order')[:2]
        return context

@require_POST
def newsletter_signup(request):
    """View for newsletter signup."""
    form = NewsletterForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors})

# Admin views for news management
class NewsCreateView(LoginRequiredMixin, CreateView):
    """View for creating news articles."""
    model = News
    form_class = NewsForm
    template_name = 'news/admin/news_form.html'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None
    
    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = None  # Inicializa self.object como None para evitar erro
        form = self.get_form()
        try:
            # Log para depuração
            print("\n\n--- DEBUG UPLOAD DE IMAGEM ---")
            if 'featured_image' in request.FILES:
                img = request.FILES['featured_image']
                print(f"Nome do arquivo: {img.name}")
                print(f"Tamanho: {img.size} bytes")
                print(f"Tipo de conteúdo: {img.content_type}")
            else:
                print("Nenhum arquivo enviado no campo 'featured_image'")
                
            if form.is_valid():
                return self.form_valid(form)
            else:
                print(f"Erros de validação do formulário: {form.errors}")
                return self.form_invalid(form)
        except Exception as e:
            import traceback
            print(f"ERRO NO UPLOAD: {str(e)}")
            print(traceback.format_exc())
            messages.error(request, f"Erro ao criar notícia: {str(e)}")
            return self.form_invalid(form)
    
    def form_valid(self, form):
        try:
            form.instance.author = self.request.user
            response = super().form_valid(form)
            # Verificamos se a imagem foi salva corretamente
            if form.instance.featured_image:
                # Registramos o caminho completo da imagem para debug
                import os
                from django.conf import settings
                full_path = os.path.join(settings.MEDIA_ROOT, str(form.instance.featured_image))
                print(f"Imagem salva em: {full_path}")
                
                # Garantimos que o arquivo existe
                if not os.path.exists(full_path):
                    print(f"ERRO: O arquivo não existe em {full_path}")
                else:
                    print(f"SUCESSO: Imagem salva corretamente em {full_path}")
                    
            messages.success(self.request, 'Notícia criada com sucesso!')
            return response
        except Exception as e:
            import traceback
            print(f"ERRO AO SALVAR: {str(e)}")
            print(traceback.format_exc())
            messages.error(self.request, f"Erro ao salvar notícia: {str(e)}")
            return self.render_to_response(self.get_context_data(form=form))
    
    def form_invalid(self, form):
        # Debug para verificar os erros de validação do formulário
        print(f"Erros no formulário: {form.errors}")
        messages.error(self.request, 'Erro ao criar notícia. Por favor, verifique os campos.')
        return super().form_invalid(form)

class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating news articles."""
    model = News
    form_class = NewsForm
    template_name = 'news/admin/news_form.html'
    
    def test_func(self):
        news = self.get_object()
        return self.request.user == news.author or self.request.user.is_staff
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Adicionar uma mensagem indicando que a imagem é opcional na edição
        form.fields['featured_image'].help_text = 'Deixe em branco para manter a imagem atual.'
        return form
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Importante definir o objeto atual
        form = self.get_form()
        
        # Verifica se uma nova imagem foi fornecida
        if not request.FILES.get('featured_image') and self.object.featured_image:
            # Se não houver nova imagem e já existir uma, mantenha a imagem atual
            form.instance.featured_image = self.object.featured_image
            # Remova erros de validação relacionados à imagem
            if 'featured_image' in form.errors:
                del form.errors['featured_image']
                
        # Verifica se o formulário é válido
        if form.is_valid():
            form.instance.author = self.request.user
            messages.success(self.request, 'Notícia atualizada com sucesso!')
            return super().form_valid(form)
        else:
            print(f"Erros de validação do formulário: {form.errors}")
            return self.form_invalid(form)

class NewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting news articles."""
    model = News
    template_name = 'news/admin/news_confirm_delete.html'
    success_url = reverse_lazy('news:admin_dashboard')
    
    def test_func(self):
        news = self.get_object()
        return self.request.user == news.author or self.request.user.is_staff

@login_required
def admin_dashboard(request):
    """View for the admin dashboard."""
    user_news = News.objects.filter(author=request.user).order_by('-created_date')
    
    context = {
        'published_count': user_news.filter(status='published').count(),
        'draft_count': user_news.filter(status='draft').count(),
        'recent_news': user_news[:10],
        'categories': Category.objects.annotate(news_count=Count('news')),
    }
    
    return render(request, 'news/admin/dashboard.html', context)

@login_required
def news_admin(request):
    """Alternative view for the admin dashboard."""
    user_news = News.objects.filter(author=request.user).order_by('-created_date')
    
    context = {
        'published_count': user_news.filter(status='published').count(),
        'draft_count': user_news.filter(status='draft').count(),
        'recent_news': user_news[:10],
        'categories': Category.objects.annotate(news_count=Count('news')),
    }
    
    return render(request, 'news/admin/dashboard.html', context)

# Views para parceiros
class PartnerListView(ListView):
    """View para listar parceiros."""
    model = Partner
    template_name = 'news/partners/partner_list.html'
    context_object_name = 'partners'
    
    def get_queryset(self):
        return Partner.objects.filter(active=True).order_by('order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        return context

class PartnerDetailView(DetailView):
    """View para detalhes de um parceiro."""
    model = Partner
    template_name = 'news/partners/partner_detail.html'
    context_object_name = 'partner'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        context['consultation_form'] = ConsultationRequestForm(initial={'partner': self.object})
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ConsultationRequestForm(request.POST)
        
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.partner = self.object
            consultation.save()
            messages.success(request, 'Sua solicitação de consulta foi enviada com sucesso! Entraremos em contato em breve.')
            return redirect('news:partner_detail', pk=self.object.pk)
        
        context = self.get_context_data(object=self.object)
        context['consultation_form'] = form
        return self.render_to_response(context)

# Views de administração para parceiros
class PartnerCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """View para criar parceiros."""
    model = Partner
    form_class = PartnerForm
    template_name = 'news/admin/partner_form.html'
    success_url = reverse_lazy('news:partner_admin')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, 'Parceiro criado com sucesso!')
        return super().form_valid(form)

class PartnerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View para atualizar parceiros."""
    model = Partner
    form_class = PartnerForm
    template_name = 'news/admin/partner_form.html'
    success_url = reverse_lazy('news:partner_admin')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, 'Parceiro atualizado com sucesso!')
        return super().form_valid(form)

class PartnerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View para excluir parceiros."""
    model = Partner
    template_name = 'news/admin/partner_confirm_delete.html'
    success_url = reverse_lazy('news:partner_admin')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Parceiro excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

@login_required
def partner_admin(request):
    """View para administração de parceiros."""
    if not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('news:home')
    
    partners = Partner.objects.all().order_by('order')
    consultation_requests = ConsultationRequest.objects.all().order_by('-created_date')
    
    context = {
        'partners': partners,
        'consultation_requests': consultation_requests,
    }
    
    return render(request, 'news/admin/partner_admin.html', context)

@login_required
def consultation_detail(request, pk):
    """View para detalhes de uma solicitação de consulta."""
    if not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('news:home')
    
    consultation = get_object_or_404(ConsultationRequest, pk=pk)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['pending', 'confirmed', 'cancelled']:
            consultation.status = status
            consultation.save()
            messages.success(request, 'Status da solicitação atualizado com sucesso!')
            return redirect('news:consultation_detail', pk=pk)
    
    context = {
        'consultation': consultation,
    }
    
    return render(request, 'news/admin/consultation_detail.html', context)

# Adicionar as views para gerenciamento de feeds RSS
class RSSFeedCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """View para criar feeds RSS."""
    model = RSSFeed
    form_class = RSSFeedForm
    template_name = 'news/admin/rss_feed_form.html'
    success_url = reverse_lazy('news:rss_feed_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, 'Feed RSS adicionado com sucesso!')
        return super().form_valid(form)

class RSSFeedUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View para atualizar feeds RSS."""
    model = RSSFeed
    form_class = RSSFeedForm
    template_name = 'news/admin/rss_feed_form.html'
    success_url = reverse_lazy('news:rss_feed_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, 'Feed RSS atualizado com sucesso!')
        return super().form_valid(form)

class RSSFeedDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View para excluir feeds RSS."""
    model = RSSFeed
    template_name = 'news/admin/rss_feed_confirm_delete.html'
    success_url = reverse_lazy('news:rss_feed_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Feed RSS excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

@login_required
def rss_feed_admin(request):
    """View para administração de feeds RSS."""
    if not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('news:home')
    
    feeds = RSSFeed.objects.all().order_by('order')
    
    context = {
        'feeds': feeds,
    }
    
    return render(request, 'news/admin/rss_feed_admin.html', context)

@staff_member_required
def rss_feed_list(request):
    """View para listar os feeds RSS."""
    feeds = RSSFeed.objects.all().order_by('order')
    
    # Contagem de feeds ativos e inativos
    active_feeds = feeds.filter(active=True).count()
    inactive_feeds = feeds.filter(active=False).count()
    
    # Lista de feeds ativos para a visualização
    active_feed_list = feeds.filter(active=True).order_by('order')
    
    context = {
        'feeds': feeds,
        'active_feeds': active_feeds,
        'inactive_feeds': inactive_feeds,
        'active_feed_list': active_feed_list,
    }
    return render(request, 'news/admin/rss_feeds.html', context)

@staff_member_required
def rss_feed_refresh(request, pk):
    """View para atualizar um feed RSS."""
    import feedparser
    
    feed = get_object_or_404(RSSFeed, pk=pk)
    
    try:
        # Atualizando feed RSS
        feedparser_data = feedparser.parse(feed.url)
        
        count = 0
        if feedparser_data.entries:
            # Limitar ao número máximo de itens do feed
            for entry in feedparser_data.entries[:feed.max_items]:
                # Lógica para processar os itens do feed (pode ser expandida conforme necessário)
                count += 1
        
        messages.success(request, f'Feed "{feed.name}" atualizado com sucesso. {count} itens processados.')
    except Exception as e:
        messages.error(request, f'Erro ao atualizar o feed: {str(e)}')
    
    return redirect('news:rss_feed_list')

@staff_member_required
def refresh_all_rss_feeds(request):
    """View para atualizar manualmente todos os feeds RSS."""
    from news.tasks import atualizar_feeds_rss
    
    # Executar a tarefa de atualização imediatamente
    result = atualizar_feeds_rss.delay()
    
    messages.success(request, 'Todos os feeds RSS estão sendo atualizados em segundo plano.')
    return redirect('news:rss_feed_list') 