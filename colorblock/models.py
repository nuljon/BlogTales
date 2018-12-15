from django.db import models
from django.shortcuts import render
from wagtail.core.blocks import FieldBlock

from colorblock.fields import ColorField, ColorWidget


class ColorBlock(FieldBlock):
    def __init__(self, required=False, help_text=None, **kwargs):
        # 'label' and 'initial' parameters are not exposed, as Block handles that functionality natively
        # (via 'label' and 'default')
        self.field = ColorField(
            required=required,
            help_text=help_text,
            widget=ColorWidget
            )
        super().__init__(**kwargs)

    class Meta:
        default = ''
        label = 'Color'
