import os
from django import template
from django.conf import settings

register = template.Library()

class TryExceptNode(template.Node):
    def __init__(self, try_nodelist, except_nodelist):
        self.try_nodelist = try_nodelist
        self.except_nodelist = except_nodelist

    def render(self, context):
        try:
            return self.try_nodelist.render(context)
        except Exception as e:
            if settings.DEBUG:
                print(f"Error in try/except template tag: {e}")
            return self.except_nodelist.render(context)

@register.tag('try')
def do_try_except(parser, token):
    """
    Tag de template que permite usar try/except em templates
    
    Uso:
    {% try %}
        {{ variavel.com.possivel.erro }}
    {% except %}
        Conteúdo para exibir em caso de erro
    {% endtry %}
    """
    try_nodelist = parser.parse(('except',))
    parser.delete_first_token()
    except_nodelist = parser.parse(('endtry',))
    parser.delete_first_token()
    return TryExceptNode(try_nodelist, except_nodelist)

@register.filter
def file_exists(filepath):
    """
    Filtro que verifica se um arquivo existe no sistema
    
    Uso:
    {% if image.path|file_exists %}
        O arquivo existe
    {% else %}
        O arquivo não existe
    {% endif %}
    """
    return os.path.exists(filepath) if filepath else False

@register.filter
def image_url_safe(image_field):
    """
    Filtro que tenta acessar a URL de uma imagem com segurança,
    retornando uma string vazia em caso de erro
    
    Uso:
    <img src="{{ news.featured_image|image_url_safe }}" alt="Imagem">
    """
    try:
        if image_field and hasattr(image_field, 'name') and image_field.name:
            return image_field.url
    except Exception as e:
        if settings.DEBUG:
            print(f"Error in image_url_safe filter: {e}")
    return "" 