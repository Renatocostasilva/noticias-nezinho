from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # Public URLs
    path('', views.HomeView.as_view(), name='home'),
    path('news/<int:year>/<int:month>/<int:day>/<slug:slug>/', 
         views.NewsDetailView.as_view(), name='news_detail'),
    path('category/<slug:slug>/', 
         views.CategoryNewsView.as_view(), name='category'),
    path('search/', 
         views.SearchResultsView.as_view(), name='search_results'),
    path('newsletter/signup/', 
         views.newsletter_signup, name='newsletter_signup'),
    
    # URLs para parceiros
    path('parceiros/', 
         views.PartnerListView.as_view(), name='partner_list'),
    path('parceiros/<int:pk>/', 
         views.PartnerDetailView.as_view(), name='partner_detail'),
    
    # Admin URLs - Renomeando para evitar conflitos
    path('news-admin/dashboard/', 
         views.admin_dashboard, name='admin_dashboard'),
    path('news-admin/', 
         views.news_admin, name='news_admin'),
    path('news-admin/news/new/', 
         views.NewsCreateView.as_view(), name='news_create'),
    path('news-admin/news/<int:pk>/edit/', 
         views.NewsUpdateView.as_view(), name='news_update'),
    path('news-admin/news/<int:pk>/delete/', 
         views.NewsDeleteView.as_view(), name='news_delete'),
         
    # Admin URLs para parceiros
    path('news-admin/parceiros/', 
         views.partner_admin, name='partner_admin'),
    path('news-admin/parceiros/novo/', 
         views.PartnerCreateView.as_view(), name='partner_create'),
    path('news-admin/parceiros/<int:pk>/editar/', 
         views.PartnerUpdateView.as_view(), name='partner_update'),
    path('news-admin/parceiros/<int:pk>/excluir/', 
         views.PartnerDeleteView.as_view(), name='partner_delete'),
    path('news-admin/consultas/<int:pk>/', 
         views.consultation_detail, name='consultation_detail'),
    
    # URLs para administração de feeds RSS
    path('news-admin/rss-feeds/', views.rss_feed_list, name='rss_feed_list'),
    path('news-admin/rss-feeds/novo/', views.RSSFeedCreateView.as_view(), name='rss_feed_create'),
    path('news-admin/rss-feeds/editar/<int:pk>/', views.RSSFeedUpdateView.as_view(), name='rss_feed_update'),
    path('news-admin/rss-feeds/excluir/<int:pk>/', views.RSSFeedDeleteView.as_view(), name='rss_feed_delete'),
    path('news-admin/rss-feeds/atualizar/<int:pk>/', views.rss_feed_refresh, name='rss_feed_refresh'),
    path('news-admin/rss-feeds/atualizar-todos/', views.refresh_all_rss_feeds, name='refresh_all_rss_feeds'),
] 