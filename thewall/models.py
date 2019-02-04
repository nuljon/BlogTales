from __future__ import unicode_literals

import datetime
from builtins import property
from datetime import date

import wagtail
from astroid import objects
from django import forms
from django.conf import settings
from django.conf.global_settings import AUTH_USER_MODEL
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.fields import CharField
from django.http import Http404, HttpResponse
from django.template.defaultfilters import first
from django.urls.base import reverse_lazy
from django.utils.dateformat import DateFormat
from django.utils.formats import date_format
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag as TaggitTag
from taggit.models import TaggedItemBase
from tinymce import AdminTinyMCE, HTMLField, TinyMCE
from wagtail import users
from wagtail.admin.edit_handlers import (FieldPanel, FieldRowPanel,
                                         InlinePanel, MultiFieldPanel,
                                         PageChooserPanel, StreamFieldPanel)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core import blocks
from wagtail.core.blocks import (CharBlock, PageChooserBlock, StructBlock,
                                 StructValue, TextBlock, URLBlock)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.fields import WagtailImageField
from wagtail.snippets.models import register_snippet

from blog.blocks import (ConstructionBlock, InlinedItemsBlock, JumbotronBlock,
                         LeftColumnWithSidebarBlock, PageHeaderBlock,
                         PageHeadingBlock, SearchBlock, SidebarBlock,
                         ThreeColumnBlock, TwoColumnBlock)


class WallPage(RoutablePageMixin, Page):

    header = StreamField(
        [('page_header', PageHeaderBlock()), ], null=True, blank=True)
    body = StreamField([('single_column', ConstructionBlock()),
                        ('column_w_sidebar', LeftColumnWithSidebarBlock()),
                        ('two_columns', TwoColumnBlock(icon="grip")),
                        ('three_columns', ThreeColumnBlock(icon="table")),
                        ('flex_row', InlinedItemsBlock()), ], null=True, blank=True)

    parent_page_types = ['home.HomePage']


    # subpage_types = []
    """
    not sure if we will have subpages, there are three way to handle this attribute:
    1. Not defining subpages means any page type can be created as a descendent.
    2. Defining the subpages restricts descendants to only classes of the defined types:
        subpage_types = ['thewall.SomePage', 'thewall.SomeOtherPage'].
    3. While defining subpages with an empty list restricts adding any descendents at all:
        subpage_types =[].
    """


    # these are the wagtail admin controls for the WallPage editor.
    # The StreamFieldPanels represent content on the page instance that will
    # preceed related non-page-model content, i.e. bricks_in_the_wall.

    content_panels = Page.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('body')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(WallPage, self).get_context(request, *args, **kwargs)
        context['bricks'] = self.bricks.all()
        context['wall_page'] = self
        context['search_type'] = getattr(self, 'search-type', "")
        context['search_term'] = getattr(self, 'search-term', "")
        context['page_author'] = self.owner
        """
        'page_author' doesn't really make sense in WallPage context since the contributed content (bricks_in_the_wall) will most likely have many authors. However, built-in structure exists in regards permissions.
            Is self.owner sufficient or must include page_author in this context?
            Do we need 'page_authors', as in a list of brick authors, whereby the 'bricks_in_the_wall' are those posts that comprise the main content of wall_page?
            Proabably the indirectly related field, brick.author, will be sufficient for use in filtering bricks by author for display or edit. This should work from another context so long as we provide for filtering bricks by parent, i.e. wall_page.
        """
        return context

    """ def get_bricks(self):
        return self.bricks.all() """


    @route(r'^(\d{4})/$')
    @route(r'^(\d{4})/(\d{2})/$')
    @route(r'^(\d{4})/(\d{2})/(\d{2})/$')
    def post_by_date(self, request, year, month=None, day=None, *args, **kwargs):
        self.bricks = self.bricks.filter(date__year=year)
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
    My blog app uses a catchall type router here for post_by_date_slug, but we are probably not going to use it here. It serves the first of posts on a date slug ... rather, we need a private access BrickMakerPage as a frontend admin screen so users can work on the db doing CRUD for thier own bricks. Only users that were logged in when posting will be able to edit their prior posted messages, i.e. "bricks". The routing for that can be handled on that BrickMakerPage model, if inheriting RoutablePageMixin, or routing by traditional url and view config files. The slug for a particular brick will likely only be useful for frontend admin and should be built from the brick pk (example: wall/brick/<int:pk>/). Backend admin will be handled by Wagtail Admin via Snippets Menu.
    """
    #@route(r'^(\d{4})/(\d{2})/(\d{2})/(.+)/$')
    #def post_by_date_slug(self, request, year, month, day, slug, *args, **kwargs):
    #    post_page = self.get_posts().filter(slug=slug).first()
    #    if not post_page:
    #        raise Http404
    #    return Page.serve(post_page, request, *args, **kwargs)

    """
    no tags are used for thewall app, yet
    """
    #@route(r'^tag/(?P<tag>[-\w]+)/$')
    #def post_by_tag(self, request, tag, *args, **kwargs):
    #    self.search_type = 'tag'
    #    self.search_term = tag
    #    self.bricks = self.bricks.filter(tags__slug=tag)
    #    return Page.serve(self, request, *args, **kwargs)
    """
    I don't think we will be using categories
    """
    #@route(r'^category/(?P<category>[-\w]+)/$')
    #def post_by_category(self, request, category, *args, **kwargs):
    #    self.search_type = 'category'
    #    self.search_term = category
    #    self.posts = self.get_posts().filter(categories__slug=category)
    #    return Page.serve(self, request, *args, **kwargs)

    @route(r'^$')
    def bricks_in_the_wall(self, request, *args, **kwargs):
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^search/$')
    def wall_search(self, request, *args, **kwargs):
        search_query = request.GET.get('q', None)
        # self.bricks = self.get_bricks()
        if search_query:
            self.bricks = self.bricks.filter(body__contains=search_query)
            self.search_term = search_query
            self.search_type = 'search'
        return Page.serve(self, request, *args, **kwargs)

# lets make some brickmakers, aka Messsage Authors, who can logon and manage their bricks.
# define a location for users to store their files
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)
# extend django User for Message Author, referred to as as Brickmaker
@register_snippet
class Brickmaker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_image = models.ImageField(upload_to=user_directory_path, blank=True)
    bio = HTMLField(blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse_lazy('BrickmakerDetail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Message Author"
        verbose_name_plural = "Message Authors"


@receiver(post_save, sender=User)
def create_brickmaker(sender, instance, created, **kwargs):
    if created:
        Brickmaker.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_brickmaker(sender, instance, **kwargs):
    instance.brickmaker.save()

# we will refer to the individual wall messages as bricks
class BrickManager(models.Manager):
    def create_brick(self, wall_page, **kwargs):
        brick = self.create(wall_page=WallPage.objects.get(pk=wall_page))
        return brick

@register_snippet
class Brick(models.Model):
    wall_page = ForeignKey(
        WallPage,
        verbose_name=('message wall'),
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
        related_name='bricks'
    )
    name = models.CharField('Name', max_length=255, blank=True)
    date = models.DateTimeField(
        verbose_name="Date", default=datetime.datetime.today)
    title = models.CharField('Title', max_length=255, default='My Title')
    content = HTMLField('Content', blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=('message author'),
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
        related_name='authored_bricks'
    )

    is_active = models.BooleanField('Active', default=True)


    def __str__(self):
        return '%s' % self.name

    def get_wall_page(self):
        return self.wall_page

    """
    I am not sure if we will need a bricks get_context method here, but we probably will need it in the BrickmakerPage model for frontend admin of bricks
"""
    def get_context_data(self, request, **kwargs):
            context = super(Brick, self).get_context_data(**kwargs)
            context['wall_page'] = self.wall_page
            context['name'] = self.name
            context['date'] = self.date
            context['title'] = self.title
            context['content'] = self.content
            context['author'] = self.author
            context['is_active'] = self.is_active
            return (request, context)

    class Meta:
        verbose_name = "Wall Message"
        verbose_name_plural = "Wall Messages"
