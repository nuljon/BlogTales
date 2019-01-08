import six
from ..models import Brick
from django.template import Library, loader, Template
from django.urls import resolve
from wagtail.core.models import Page


register = Library()


@register.inclusion_tag('thewall/parts/bricks_in_the_wall.html', takes_context=True)
def bricks_in_the_wall(context):
    wall_page = context['wall_page']
    brick = context['brick']
    bricks_in_the_wall = wall_page.bricks.all()
    return {'wall_page': wall_page, 'bricks_in_the_wall': bricks_in_the_wall, 'request': context['request']}
