from __future__ import unicode_literals
import datetime
from datetime import date

import wagtail

from django import forms
from django.conf.global_settings import AUTH_USER_MODEL
from django.contrib.auth.models import User
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, \
    InlinePanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

from blog.models import LandingPage


class HomePage(Page):
    subpage_types = ['blog.LandingPage', 'blog.BlogPage']
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]
