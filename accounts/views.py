from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, 
    PasswordResetView, PasswordResetConfirmView
)
from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm, 
    CustomPasswordChangeForm, CustomPasswordResetForm, 
    CustomSetPasswordForm, UserProfileForm
)
from news.models import Comment, News

class SignUpView(CreateView):
    """View for user registration."""
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your account has been created successfully! You can now log in.')
        return response

class CustomLoginView(LoginView):
    """Custom login view."""
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    
    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me', False)
        if not remember_me:
            # Session expires when the user closes the browser
            self.request.session.set_expiry(0)
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    """Custom logout view."""
    next_page = reverse_lazy('news:home')

class CustomPasswordChangeView(PasswordChangeView):
    """Custom password change view."""
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:password_change_done')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your password has been changed successfully!')
        return response

class CustomPasswordResetView(PasswordResetView):
    """Custom password reset view."""
    form_class = CustomPasswordResetForm
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Custom password reset confirm view."""
    form_class = CustomSetPasswordForm
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

@login_required
def profile(request):
    """View para o perfil do usuário."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    # Não vamos mais buscar comentários do usuário aqui, pois o modelo Comment não tem campo user
    # Vamos deixar a lista vazia por enquanto
    user_comments = []
    
    # Obter notícias favoritas (implementação futura)
    favorite_news = []
    
    context = {
        'form': form,
        'user_comments': user_comments,
        'favorite_news': favorite_news,
    }
    return render(request, 'accounts/profile.html', context) 