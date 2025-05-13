#!/usr/bin/env python
"""
Script para inicializar o banco de dados com dados de exemplo.
Execute este script após resetar o banco de dados e criar um superusuário.
"""
import os
import sys
import django

# Configura o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noticias.settings')
django.setup()

from django.contrib.auth.models import User
from news.models import Category, News
from django.utils import timezone
from django.core.files.images import ImageFile
from django.core.files.temp import NamedTemporaryFile
import requests
import random
from urllib.parse import urlparse

def download_image(url):
    """Baixa uma imagem da internet e retorna um objeto ImageFile."""
    response = requests.get(url)
    if response.status_code != 200:
        return None
    
    # Extrai o nome do arquivo da URL
    filename = os.path.basename(urlparse(url).path)
    
    # Cria um arquivo temporário
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(response.content)
    img_temp.flush()
    
    return ImageFile(img_temp, name=filename)

def create_categories():
    """Cria categorias de exemplo."""
    categories = [
        {'name': 'Política', 'color': '#dc3545'},
        {'name': 'Economia', 'color': '#28a745'},
        {'name': 'Tecnologia', 'color': '#007bff'},
        {'name': 'Esportes', 'color': '#fd7e14'},
        {'name': 'Entretenimento', 'color': '#6f42c1'},
        {'name': 'Saúde', 'color': '#20c997'},
    ]
    
    created_categories = []
    for category_data in categories:
        category, created = Category.objects.get_or_create(
            name=category_data['name'],
            defaults={'color': category_data['color']}
        )
        created_categories.append(category)
        if created:
            print(f"Categoria '{category.name}' criada com sucesso!")
        else:
            print(f"Categoria '{category.name}' já existe.")
    
    return created_categories

def create_news(categories, author):
    """Cria notícias de exemplo."""
    # Imagens de exemplo (placeholders)
    image_urls = [
        'https://picsum.photos/800/600?random=1',
        'https://picsum.photos/800/600?random=2',
        'https://picsum.photos/800/600?random=3',
        'https://picsum.photos/800/600?random=4',
        'https://picsum.photos/800/600?random=5',
    ]
    
    # Notícias de exemplo
    news_data = [
        {
            'title': 'Governo anuncia novo pacote de medidas econômicas',
            'content': '<p>O governo anunciou hoje um novo pacote de medidas econômicas que visa estimular o crescimento e reduzir o desemprego. Entre as medidas estão a redução de impostos para pequenas empresas, incentivos fiscais para contratação de jovens e investimentos em infraestrutura.</p><p>Segundo o ministro da Economia, as medidas devem gerar cerca de 500 mil novos empregos nos próximos 12 meses e aumentar o PIB em 2%.</p><p>"Estamos confiantes de que estas medidas vão impulsionar a economia e melhorar a vida dos brasileiros", afirmou o ministro durante coletiva de imprensa.</p>',
            'category': 'Política',
            'is_featured': True,
            'is_slider': True,
            'is_trending': True,
        },
        {
            'title': 'Bolsa de valores atinge novo recorde histórico',
            'content': '<p>A bolsa de valores atingiu hoje um novo recorde histórico, impulsionada por resultados positivos de empresas do setor financeiro e de tecnologia. O índice principal subiu 2,5%, fechando o dia nos 130 mil pontos.</p><p>Analistas atribuem o bom desempenho à melhora nas expectativas econômicas e ao fluxo de capital estrangeiro que tem entrado no país nas últimas semanas.</p><p>"O mercado está otimista com as perspectivas de crescimento econômico e com a estabilidade política", comentou um analista de mercado.</p>',
            'category': 'Economia',
            'is_featured': True,
            'is_slider': False,
            'is_trending': True,
        },
        {
            'title': 'Nova tecnologia promete revolucionar o tratamento de câncer',
            'content': '<p>Pesquisadores desenvolveram uma nova tecnologia que promete revolucionar o tratamento de câncer. A inovação utiliza inteligência artificial para identificar células cancerígenas com precisão muito maior que os métodos atuais.</p><p>Os testes iniciais mostraram uma eficácia de 95% na detecção precoce de tumores, o que pode aumentar significativamente as chances de cura.</p><p>"Esta tecnologia representa um avanço significativo na luta contra o câncer", afirmou o líder da pesquisa.</p>',
            'category': 'Tecnologia',
            'is_featured': True,
            'is_slider': True,
            'is_trending': False,
        },
        {
            'title': 'Seleção brasileira se prepara para Copa do Mundo',
            'content': '<p>A seleção brasileira iniciou hoje os preparativos para a próxima Copa do Mundo. Os jogadores se apresentaram no centro de treinamento e participaram das primeiras atividades sob o comando do técnico.</p><p>O Brasil está no Grupo C da competição e estreia contra a Suíça no dia 17 de junho.</p><p>"Estamos muito motivados e confiantes. Vamos trabalhar duro para trazer o hexa para o Brasil", declarou o capitão da equipe.</p>',
            'category': 'Esportes',
            'is_featured': False,
            'is_slider': True,
            'is_trending': True,
        },
        {
            'title': 'Festival de cinema anuncia filmes selecionados',
            'content': '<p>O Festival Internacional de Cinema anunciou hoje os filmes selecionados para a edição deste ano. Ao todo, serão exibidos 120 filmes de 35 países diferentes.</p><p>Entre os destaques estão produções premiadas em outros festivais e obras de diretores renomados.</p><p>O festival acontece entre os dias 10 e 20 de setembro e os ingressos já estão à venda.</p>',
            'category': 'Entretenimento',
            'is_featured': True,
            'is_slider': False,
            'is_trending': False,
        },
        {
            'title': 'Estudo revela benefícios da meditação para a saúde mental',
            'content': '<p>Um novo estudo científico revelou que a prática regular de meditação pode reduzir significativamente os níveis de ansiedade e estresse.</p><p>A pesquisa, que acompanhou 500 participantes durante seis meses, mostrou que aqueles que meditavam por pelo menos 15 minutos diários apresentaram uma redução de 30% nos sintomas de ansiedade.</p><p>"A meditação é uma ferramenta poderosa e acessível para melhorar a saúde mental", afirmou a coordenadora do estudo.</p>',
            'category': 'Saúde',
            'is_featured': False,
            'is_slider': False,
            'is_trending': True,
        },
    ]
    
    created_news = []
    for news_item in news_data:
        # Encontra a categoria
        category = next((c for c in categories if c.name == news_item['category']), None)
        if not category:
            print(f"Categoria '{news_item['category']}' não encontrada. Pulando notícia.")
            continue
        
        # Baixa uma imagem aleatória
        image_url = random.choice(image_urls)
        try:
            image = download_image(image_url)
            if not image:
                print(f"Erro ao baixar imagem de {image_url}. Pulando notícia.")
                continue
        except Exception as e:
            print(f"Erro ao baixar imagem: {e}. Pulando notícia.")
            continue
        
        # Cria a notícia
        news, created = News.objects.get_or_create(
            title=news_item['title'],
            defaults={
                'content': news_item['content'],
                'author': author,
                'category': category,
                'featured_image': image,
                'status': 'published',
                'is_featured': news_item['is_featured'],
                'is_slider': news_item['is_slider'],
                'is_trending': news_item['is_trending'],
                'publish_date': timezone.now(),
            }
        )
        
        if created:
            # Adiciona algumas tags
            news.tags.add('exemplo', news_item['category'].lower(), 'destaque')
            created_news.append(news)
            print(f"Notícia '{news.title}' criada com sucesso!")
        else:
            print(f"Notícia '{news.title}' já existe.")
    
    return created_news

def main():
    """Função principal."""
    print("Inicializando o banco de dados com dados de exemplo...")
    
    # Verifica se existe pelo menos um superusuário
    if not User.objects.filter(is_superuser=True).exists():
        print("Nenhum superusuário encontrado. Por favor, crie um superusuário primeiro.")
        print("Execute: python manage.py createsuperuser")
        return
    
    # Obtém o primeiro superusuário
    author = User.objects.filter(is_superuser=True).first()
    print(f"Usando o usuário '{author.username}' como autor das notícias.")
    
    # Cria categorias
    categories = create_categories()
    
    # Cria notícias
    news = create_news(categories, author)
    
    print(f"\nInicialização concluída!")
    print(f"Foram criadas {len(categories)} categorias e {len(news)} notícias.")
    print("\nAgora você pode executar o servidor Django com o comando:")
    print("python manage.py runserver")

if __name__ == "__main__":
    main() 