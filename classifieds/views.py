from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from .models import Ad, Photo, ContactMessage
from .forms import AdForm, ContactForm, PaymentForm

def classified_list(request):
    """Exibe a lista de anúncios aprovados"""
    ads = Ad.objects.filter(status='approved')
    
    paginator = Paginator(ads, 12)  # 12 anúncios por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'classifieds/ad_list.html', {
        'page_obj': page_obj,
    })

def ad_detail(request, ad_id):
    """Exibe os detalhes de um anúncio"""
    ad = get_object_or_404(Ad, id=ad_id, status='approved')
    
    # Formulário de contato
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.ad = ad
            message.save()
            
            # Enviar email para o anunciante
            try:
                send_mail(
                    f'Nova mensagem sobre seu anúncio: {ad.title}',
                    f'Você recebeu uma mensagem de {message.sender_name} ({message.sender_email}):\n\n{message.message}',
                    settings.DEFAULT_FROM_EMAIL,
                    [ad.email],
                    fail_silently=False,
                )
                messages.success(request, 'Sua mensagem foi enviada com sucesso!')
            except:
                messages.warning(request, 'Sua mensagem foi recebida, mas houve um problema ao enviar o email de notificação.')
            
            return redirect('classifieds:ad_detail', ad_id=ad.id)
    else:
        form = ContactForm()
    
    return render(request, 'classifieds/ad_detail.html', {
        'ad': ad,
        'form': form,
    })

def ad_create(request):
    """Cria um novo anúncio"""
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            # Salvar o anúncio
            ad = form.save(commit=False)
            ad.status = 'pending'
            ad.save()
            
            # Processar a foto, se enviada
            if 'photos' in request.FILES:
                photo = request.FILES['photos']
                photo_obj = Photo(image=photo)
                photo_obj.save()
                ad.photos.add(photo_obj)
            
            # Verificar se o usuário quer destacar o anúncio
            if form.cleaned_data.get('highlight'):
                return redirect('classifieds:payment', ad_id=ad.id)
            
            messages.success(request, 'Seu anúncio foi enviado e está aguardando aprovação.')
            return redirect('classifieds:ad_list')
    else:
        form = AdForm()
    
    return render(request, 'classifieds/ad_form.html', {
        'form': form,
    })

def payment(request, ad_id):
    """Simulação de pagamento para destacar anúncio"""
    ad = get_object_or_404(Ad, id=ad_id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Simulação de processamento de pagamento
            ad.highlight = True
            ad.save()
            
            messages.success(request, 'Pagamento processado com sucesso! Seu anúncio será destacado após aprovação.')
            return redirect('classifieds:ad_list')
    else:
        form = PaymentForm()
    
    return render(request, 'classifieds/payment.html', {
        'form': form,
        'ad': ad,
    })

@login_required
def my_ads(request):
    """Exibe os anúncios do usuário logado (para implementação futura)"""
    # Esta função seria implementada se os anúncios fossem associados a usuários
    pass

def staff_check(user):
    """Verifica se o usuário é membro da equipe."""
    return user.is_staff

@login_required
@user_passes_test(staff_check)
def admin_dashboard(request):
    """Painel de administração para classificados."""
    # Obter todos os anúncios, ordenados por data de criação (mais recentes primeiro)
    ads = Ad.objects.all().order_by('-created_at')
    
    # Filtrar por status, se especificado
    status_filter = request.GET.get('status')
    if status_filter and status_filter != 'all':
        ads = ads.filter(status=status_filter)
    
    # Filtrar por destaque, se especificado
    highlight_filter = request.GET.get('highlight')
    if highlight_filter:
        if highlight_filter == 'yes':
            ads = ads.filter(highlight=True)
        elif highlight_filter == 'no':
            ads = ads.filter(highlight=False)
    
    # Paginação
    paginator = Paginator(ads, 10)  # 10 anúncios por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas
    stats = {
        'total': Ad.objects.count(),
        'pending': Ad.objects.filter(status='pending').count(),
        'approved': Ad.objects.filter(status='approved').count(),
        'rejected': Ad.objects.filter(status='rejected').count(),
        'highlighted': Ad.objects.filter(highlight=True).count(),
    }
    
    return render(request, 'classifieds/admin/dashboard.html', {
        'page_obj': page_obj,
        'stats': stats,
        'status_filter': status_filter,
        'highlight_filter': highlight_filter,
    })

@login_required
@user_passes_test(staff_check)
def admin_ad_detail(request, ad_id):
    """Detalhes de um anúncio no painel de administração."""
    ad = get_object_or_404(Ad, id=ad_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            ad.status = 'approved'
            ad.save()
            messages.success(request, f'O anúncio "{ad.title}" foi aprovado com sucesso.')
        elif action == 'reject':
            ad.status = 'rejected'
            ad.save()
            messages.success(request, f'O anúncio "{ad.title}" foi rejeitado.')
        elif action == 'highlight':
            ad.highlight = True
            ad.save()
            messages.success(request, f'O anúncio "{ad.title}" foi destacado.')
        elif action == 'remove_highlight':
            ad.highlight = False
            ad.save()
            messages.success(request, f'O destaque do anúncio "{ad.title}" foi removido.')
        elif action == 'delete':
            ad.delete()
            messages.success(request, f'O anúncio "{ad.title}" foi excluído permanentemente.')
            return redirect('classifieds:admin_dashboard')
        elif action == 'delete_photo':
            photo_id = request.POST.get('photo_id')
            if photo_id:
                try:
                    photo = Photo.objects.get(id=photo_id)
                    if photo in ad.photos.all():
                        ad.photos.remove(photo)
                        photo.delete()
                        messages.success(request, f'A foto foi removida do anúncio.')
                    else:
                        messages.error(request, f'A foto não pertence a este anúncio.')
                except Photo.DoesNotExist:
                    messages.error(request, f'Foto não encontrada.')
        elif action == 'add_photo':
            if 'image' in request.FILES:
                try:
                    # Verificar se o anúncio já tem 5 fotos
                    if ad.photos.count() >= 5:
                        messages.error(request, f'Este anúncio já possui o número máximo de 5 fotos.')
                    else:
                        image = request.FILES['image']
                        photo = Photo(image=image)
                        photo.save()
                        ad.photos.add(photo)
                        messages.success(request, f'Foto adicionada com sucesso ao anúncio.')
                except Exception as e:
                    messages.error(request, f'Erro ao adicionar foto: {str(e)}')
            else:
                messages.error(request, f'Nenhuma imagem foi enviada.')
        
        return redirect('classifieds:admin_ad_detail', ad_id=ad.id)
    
    # Obter mensagens de contato relacionadas a este anúncio
    contact_messages = ContactMessage.objects.filter(ad=ad).order_by('-created_at')
    
    return render(request, 'classifieds/admin/ad_detail.html', {
        'ad': ad,
        'contact_messages': contact_messages,
    })
