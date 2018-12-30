from __future__ import unicode_literals
import datetime
from datetime import date

import wagtail
from astroid import objects
from django import forms
from django.conf.global_settings import AUTH_USER_MODEL
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import Http404, HttpResponse
from django.template.defaultfilters import first
from django.utils.dateformat import DateFormat
from django.utils.formats import date_format
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag as TaggitTag, TaggedItemBase
from tinymce import AdminTinyMCE, HTMLField, TinyMCE
from wagtail import users
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, \
    InlinePanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core import blocks
from wagtail.core.blocks import CharBlock, PageChooserBlock, StructBlock, \
    StructValue, TextBlock, URLBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from blog.blocks import ConstructionBlock, InlinedItemsBlock, JumbotronBlock, \
    LeftColumnWithSidebarBlock, PageHeaderBlock, PageHeadingBlock, \
    SearchBlock, SidebarBlock, ThreeColumnBlock, TwoColumnBlock


class WallPage(RoutablePageMixin, Page):
    header = StreamField(
        [('page_header', PageHeaderBlock()), ], null=True, blank=True)
    body = StreamField([('single_column', ConstructionBlock()),
                        ('column_w_sidebar', LeftColumnWithSidebarBlock()),
                        ('two_columns', TwoColumnBlock(icon="grip")),
                        ('three_columns', ThreeColumnBlock(icon="table")),
                        ('flex_row', InlinedItemsBlock()), ], null=True, blank=True)

    parent_page_types = ['home.HomePage']

    """
    subpage_types
    not sure if we will have subpages, there are three way to handle this attribute:
    1. Not defining subpages means any page type can be created as a descendent.
    2. Defining the subpages restricts descendants to only classes of the defined types:
        subpage_types = ['thewall.SomePage', 'thewall.SomeOtherPage'].
    3. While defining subpages with an empty list restrict adding any descendents at all:
        subpage_types =[].
    """
    """
    eventually, I think content will need to be manged from a form or maybe django admin. Unless I can get the bricks to work in wagtail with ModelAdmin and ModelCluster
    """
    content_panels = Page.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('body')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(WallPage, self).get_context(request, *args, **kwargs)
        context['bricks'] = self.get_bricks()
        context['wall_page'] = self
        context['search_type'] = getattr(self, 'search-type', "")
        context['search_term'] = getattr(self, 'search-term', "")
        context['page_author'] = self.owner
        """
        'page_author' doesn't really make sense except in regards permissions and self.owner is probably sufficient. Do we need 'page_authors', as in a list of brick authors, whereby the bricks are those posts that comprise the wall_page? Probably, but rather for use in seaching bricks by brick_author
        """
        return context

    """
   we may use descendant_of we will if get MPT of some sort working for bricks
   """
    def get_bricks(self):
        return Brick.objects.all()


    @route(r'^(\d{4})/$')
    @route(r'^(\d{4})/(\d{2})/$')
    @route(r'^(\d{4})/(\d{2})/(\d{2})/$')
    def post_by_date(self, request, year, month=None, day=None, *args, **kwargs):
        self.bricks = self.get_bricks().filter(date__year=year)
        self.search_type = 'date'
        self.search_term = year
        if month:
            self.bricks = self.bricks.filter(date__month=month)
            df = DateFormat(date(int(year), int(month), 1))
            self.search_term = df.format('F Y')
        if day:
            self.bricks = self.bricks.filter(date__day=day)
            self.search_term = date_format(
                date(int(year), int(month), int(day)))
        return Page.serve(self, request, *args, **kwargs)

    """
    probably not date slug here and certainly not the first of posts on a date ... thinking we need a BrickMakerPage for CRUD of bricks by brick_owner - this will be a Front-end facing form using the tiny MCE 4 app. So, users will be able to customize their memorial "bricks" that are posted to the "wall". The slug should be auto generated as a canonical URL for the "wall" page with a custom target built from the brick pk (example: https://nuljonapp.pythonanyware.com/thewall/#brick_pk)
    @route(r'^(\d{4})/(\d{2})/(\d{2})/(.+)/$')
    def post_by_date_slug(self, request, year, month, day, slug, *args, **kwargs):
        post_page = self.get_posts().filter(slug=slug).first()
        if not post_page:
            raise Http404
        return Page.serve(post_page, request, *args, **kwargs)
    """
    """
    we will probably assign tags programmatically based on media type so we need to search for them
    """
    @route(r'^tag/(?P<tag>[-\w]+)/$')
    def post_by_tag(self, request, tag, *args, **kwargs):
        self.search_type = 'tag'
        self.search_term = tag
        self.bricks = self.get_bricks().filter(tags__slug=tag)
        return Page.serve(self, request, *args, **kwargs)
    """
    I don't think we will be using categories
    @route(r'^category/(?P<category>[-\w]+)/$')
    def post_by_category(self, request, category, *args, **kwargs):
        self.search_type = 'category'
        self.search_term = category
        self.posts = self.get_posts().filter(categories__slug=category)
        return Page.serve(self, request, *args, **kwargs)
    """

    @route(r'^$')
    def brick_list(self, request, *args, **kwargs):
        self.bricks = self.get_bricks()
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^search/$')
    def wall_search(self, request, *args, **kwargs):
        search_query = request.GET.get('q', None)
        self.bricks = self.get_bricks()
        if search_query:
            self.bricks = self.bricks.filter(body__contains=search_query)
            self.search_term = search_query
            self.search_type = 'search'
        return Page.serve(self, request, *args, **kwargs)

@register_snippet
class Brick(models.Model):
    wall_page = ParentalKey(
         WallPage, related_name='bricks', on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=255, blank=True)
    date = models.DateTimeField(
        verbose_name="Date", default=datetime.datetime.today)
    title = models.CharField('Title', max_length=255, default='My Title')
    content = HTMLField('Content', blank=True)
    author = models.CharField('Author', max_length=255, default='anonymous')

    def __str__(self):
        return '%s' % self.name

    @property
    def get_wall_pages(self):
        return WallPage.objects.all()

    """
    def get_context(self, request, *args, **kwargs):
        context = super(Brick, self).get_context(
            request, *args, **kwargs)
        context['author'] = self.author
        context['wall_page'] = self.wall_page
        return context """

    class Meta:
        verbose_name = "Wall Message"
        verbose_name_plural = "Wall Messages"







