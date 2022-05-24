#!/usr/bin/env python

import re
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.forms import *
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _


color_re = re.compile('^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
validate_color = RegexValidator(color_re, _('Enter a valid color.'), 'invalid')


class ColorWidget(TextInput):
    class Media:
        if settings.DEBUG:
            js = ['colorblock/js/colors.js','colorblock/js/jqColorPicker.js' ]
        else:
            js = ['colorblock/js/colors.js', 'colorblock/js/jqColorPicker.js']



    def __init__(self, attrs=None):
        self.attrs = attrs
        super(ColorWidget, self).__init__(attrs=attrs)

    def render(self, prefix, field_value, attrs={}, renderer=None, **_kwargs):
        attrs.update(self.attrs)
        value = field_value
        name = prefix
        is_required = self.is_required
        rendered = super(ColorWidget, self).render(
            name, value, attrs={}, renderer=None, **_kwargs)
        return render_to_string('colorblock/color.html', locals() )


    def value_from_datadict(self, data, files, name):
        ret = super(ColorWidget, self).value_from_datadict(data, files, name)
        # Add a hash mark if needed so browser reads value as hex code for color
        if ret.startswith('#'):
            return ret
        ret = f'#{ret}' if ret else ret
        return ret


class ColorField(CharField):
    widget = ColorWidget
    default_validators = [validate_color]

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 18
        super(ColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = self.widget
        return super(ColorField, self).formfield(**kwargs)

    def required(self):
        return False


    def prepare_value(self, value):
        if isinstance(value, str):
            return value[1:] if value.startswith('#') else value
        # return str(value)
        # or should it be
        return self.prepare_value(str(value))