import six
from ..models import Brick
from django.template import Library, loader, Template
from django.urls import resolve
from wagtail.core.models import Page


register = Library()


