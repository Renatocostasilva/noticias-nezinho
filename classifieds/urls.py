from django.urls import path
from . import views

app_name = 'classifieds'

urlpatterns = [
    path('', views.classified_list, name='ad_list'),
    path('anuncio/<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('anuncio/novo/', views.ad_create, name='ad_create'),
    path('anuncio/<int:ad_id>/pagamento/', views.payment, name='payment'),
    path('meus-anuncios/', views.my_ads, name='my_ads'),
    
    # URLs do painel de administração
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/anuncio/<int:ad_id>/', views.admin_ad_detail, name='admin_ad_detail'),
] 