#!/usr/bin/env python
import os
import django
import random
from datetime import timedelta
from django.utils import timezone
from django.core.files.images import ImageFile

# Configurar ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noticias.settings')
django.setup()

# Importar modelos após configuração do Django
from classifieds.models import Ad, Photo, ContactMessage
from django.contrib.auth.models import User

def criar_anuncios_exemplo():
    """
    Cria anúncios de exemplo para demonstração da seção de classificados.
    Inclui anúncios em diferentes estados (pendente, aprovado, rejeitado)
    e alguns com destaque.
    """
    print("Iniciando criação de anúncios de exemplo...")
    
    # Categorias disponíveis
    categorias = ['imoveis', 'veiculos', 'eletronicos', 'moveis', 'empregos', 'servicos', 'outros']
    
    # Dados de exemplo para anúncios
    anuncios_dados = [
        {
            'titulo': 'Apartamento 2 quartos no Centro',
            'descricao': 'Ótimo apartamento com 2 quartos, sala ampla, cozinha planejada e área de serviço.',
            'nome': 'Carlos Silva',
            'email': 'carlos@exemplo.com',
            'telefone': '(11) 98765-4321',
            'status': 'approved',
            'destaque': True,
            'imagens': ['media/sample_images/apartamento.jpg']
        },
        {
            'titulo': 'Honda Civic 2019 completo',
            'descricao': 'Honda Civic 2019, completo, único dono, apenas 30.000 km rodados. IPVA 2023 pago.',
            'nome': 'Ana Oliveira',
            'email': 'ana@exemplo.com',
            'telefone': '(11) 91234-5678',
            'status': 'approved',
            'destaque': True,
            'imagens': ['media/sample_images/carro.jpg']
        },
        {
            'titulo': 'iPhone 13 128GB novo lacrado',
            'descricao': 'iPhone 13 128GB, novo, lacrado na caixa. Garantia Apple de 1 ano.',
            'nome': 'Pedro Santos',
            'email': 'pedro@exemplo.com',
            'telefone': '(11) 97777-8888',
            'status': 'approved',
            'destaque': True,
            'imagens': ['media/sample_images/iphone.jpg']
        },
        {
            'titulo': 'Sofá 3 lugares retrátil',
            'descricao': 'Sofá retrátil de 3 lugares, tecido suede, cor cinza, semi-novo.',
            'nome': 'Mariana Costa',
            'email': 'mariana@exemplo.com',
            'telefone': '(11) 95555-6666',
            'status': 'approved',
            'destaque': False,
            'imagens': ['media/sample_images/sofa.jpg']
        },
        {
            'titulo': 'Vaga para desenvolvedor Python',
            'descricao': 'Empresa de tecnologia busca desenvolvedor Python com experiência em Django. Salário a combinar.',
            'nome': 'RH Tech Solutions',
            'email': 'rh@techsolutions.com',
            'telefone': '(11) 3333-4444',
            'status': 'approved',
            'destaque': False,
            'imagens': []
        },
        {
            'titulo': 'Serviços de jardinagem',
            'descricao': 'Ofereço serviços de jardinagem, poda de árvores, plantio e manutenção de jardins.',
            'nome': 'José Pereira',
            'email': 'jose@exemplo.com',
            'telefone': '(11) 92222-3333',
            'status': 'pending',
            'destaque': False,
            'imagens': ['media/sample_images/jardinagem.jpg']
        },
        {
            'titulo': 'Guitarra Fender Stratocaster',
            'descricao': 'Guitarra Fender Stratocaster mexicana, cor sunburst, com case rígido.',
            'nome': 'Lucas Mendes',
            'email': 'lucas@exemplo.com',
            'telefone': '(11) 94444-5555',
            'status': 'rejected',
            'destaque': False,
            'imagens': ['media/sample_images/guitarra.jpg']
        },
        {
            'titulo': 'Notebook Dell Inspiron',
            'descricao': 'Notebook Dell Inspiron, i5 10ª geração, 8GB RAM, SSD 256GB, tela 15.6".',
            'nome': 'Fernanda Lima',
            'email': 'fernanda@exemplo.com',
            'telefone': '(11) 96666-7777',
            'status': 'approved',
            'destaque': True,
            'imagens': ['media/sample_images/notebook.jpg']
        }
    ]
    
    # Criar diretório para imagens de exemplo se não existir
    sample_images_dir = 'media/sample_images'
    os.makedirs(sample_images_dir, exist_ok=True)
    
    # Verificar se já existem anúncios
    if Ad.objects.exists():
        print("Já existem anúncios no banco de dados, mas vamos criar novos exemplos.")
        # Não retornar aqui para permitir a criação de novos anúncios
    
    # Criar anúncios
    anuncios_criados = 0
    for dados in anuncios_dados:
        # Selecionar categoria
        categoria = dados['categoria'] if dados['categoria'] in categorias else random.choice(categorias)
        
        # Criar anúncio
        anuncio = Ad.objects.create(
            title=dados['titulo'],
            description=dados['descricao'],
            name=dados['nome'],
            email=dados['email'],
            phone=dados['telefone'],
            status=dados['status'],
            highlight=dados['destaque'],
            created_at=timezone.now() - timedelta(days=random.randint(1, 30)),
            updated_at=timezone.now() - timedelta(days=random.randint(0, 5))
        )
        
        # Adicionar imagens se disponíveis
        for imagem_path in dados['imagens']:
            try:
                # Verificar se o arquivo existe
                if os.path.exists(imagem_path):
                    with open(imagem_path, 'rb') as img_file:
                        photo = Photo(ad=anuncio)
                        photo.image.save(
                            os.path.basename(imagem_path),
                            ImageFile(img_file),
                            save=True
                        )
                        # Adicionar a foto ao anúncio
                        anuncio.photos.add(photo)
                else:
                    print(f"Arquivo de imagem não encontrado: {imagem_path}")
            except Exception as e:
                print(f"Erro ao adicionar imagem ao anúncio {anuncio.id}: {e}")
        
        # Adicionar mensagens de contato para alguns anúncios
        if random.random() > 0.5:
            num_mensagens = random.randint(1, 3)
            for i in range(num_mensagens):
                ContactMessage.objects.create(
                    ad=anuncio,
                    sender_name=f"Contato {i+1}",
                    sender_email=f"contato{i+1}@exemplo.com",
                    message=f"Olá, tenho interesse no seu anúncio. Poderia me dar mais informações? Mensagem {i+1}",
                    created_at=timezone.now() - timedelta(days=random.randint(0, 10))
                )
        
        anuncios_criados += 1
        print(f"Anúncio criado: {anuncio.title} (ID: {anuncio.id})")
    
    print(f"\nTotal de anúncios criados: {anuncios_criados}")
    print("Criação de anúncios de exemplo concluída!")

if __name__ == "__main__":
    criar_anuncios_exemplo() 