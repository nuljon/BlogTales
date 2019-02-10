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
from wagtail.core.blocks import CharBlock, PageChooserBlock, StructBlock, StructValue, TextBlock, URLBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from blog.models import BlogPage, LandingPage
from blog.blocks import ConstructionBlock, InlinedItemsBlock, JumbotronBlock, LeftColumnWithSidebarBlock, PageHeadingBlock, SearchBlock, SidebarBlock, ThreeColumnBlock, TwoColumnBlock, PageHeaderBlock


class HomePage(Page):

    header = StreamField(
        [('page_header', PageHeaderBlock()), ], null=True, blank=True)
    body = StreamField([('single_column', ConstructionBlock()),
                        ('column_w_sidebar', LeftColumnWithSidebarBlock()),
                        ('two_columns', TwoColumnBlock(icon="grip")),
                        ('three_columns', ThreeColumnBlock(icon="table")),
                        ('flex_row', InlinedItemsBlock()), ], null=True, blank=True)


    subpage_types = ['blog.LandingPage', 'blog.BlogPage', 'thewall.WallPage']

    content_panels = Page.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('body')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(HomePage, self).get_context(request, *args, **kwargs)
        context['page_author'] = self.owner
        context['menuitems'] = self.get_children().filter(
            live=True, show_in_menus=True)
        return context

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Home"
        verbose_name_plural = "Home"

