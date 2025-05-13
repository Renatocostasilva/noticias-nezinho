#!/usr/bin/env python
import os
import django
from django.utils import timezone

# Configurar ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noticias.settings')
django.setup()

# Importar modelos após configuração do Django
from classifieds.models import Ad, Photo, ContactMessage

def criar_anuncios_exemplo():
    """Cria anúncios de exemplo para demonstração da seção de classificados."""
    print("Iniciando criação de anúncios de exemplo...")
    
    # Criar anúncios
    anuncio1 = Ad.objects.create(
        title="Apartamento 2 quartos no Centro",
        description="Ótimo apartamento com 2 quartos, sala ampla, cozinha planejada e área de serviço.",
        name="Carlos Silva",
        email="carlos@exemplo.com",
        phone="(11) 98765-4321",
        status="approved",
        highlight=True
    )
    print(f"Anúncio criado: {anuncio1.title} (ID: {anuncio1.id})")
    
    anuncio2 = Ad.objects.create(
        title="Honda Civic 2019 completo",
        description="Honda Civic 2019, completo, único dono, apenas 30.000 km rodados. IPVA 2023 pago.",
        name="Ana Oliveira",
        email="ana@exemplo.com",
        phone="(11) 91234-5678",
        status="approved",
        highlight=True
    )
    print(f"Anúncio criado: {anuncio2.title} (ID: {anuncio2.id})")
    
    anuncio3 = Ad.objects.create(
        title="iPhone 13 128GB novo lacrado",
        description="iPhone 13 128GB, novo, lacrado na caixa. Garantia Apple de 1 ano.",
        name="Pedro Santos",
        email="pedro@exemplo.com",
        phone="(11) 97777-8888",
        status="approved",
        highlight=True
    )
    print(f"Anúncio criado: {anuncio3.title} (ID: {anuncio3.id})")
    
    anuncio4 = Ad.objects.create(
        title="Serviços de jardinagem",
        description="Ofereço serviços de jardinagem, poda de árvores, plantio e manutenção de jardins.",
        name="José Pereira",
        email="jose@exemplo.com",
        phone="(11) 92222-3333",
        status="pending",
        highlight=False
    )
    print(f"Anúncio criado: {anuncio4.title} (ID: {anuncio4.id})")
    
    # Adicionar mensagem de contato para um anúncio
    ContactMessage.objects.create(
        ad=anuncio1,
        sender_name="Interessado",
        sender_email="interessado@exemplo.com",
        message="Olá, tenho interesse no seu apartamento. Poderia me dar mais informações sobre a localização?"
    )
    print("Mensagem de contato adicionada para o anúncio 1")
    
    print("\nTotal de anúncios criados: 4")
    print("Criação de anúncios de exemplo concluída!")

if __name__ == "__main__":
    criar_anuncios_exemplo() 