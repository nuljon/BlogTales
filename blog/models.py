from __future__ import unicode_literals
import datetime
from datetime import date

import wagtail

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
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag as TaggitTag, TaggedItemBase
from wagtail import users
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core import blocks
from wagtail.core.blocks import CharBlock, PageChooserBlock, StructBlock, StructValue, TextBlock, URLBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from blog.blocks import ConstructionBlock, InlinedItemsBlock, JumbotronBlock, LeftColumnWithSidebarBlock, PageHeadingBlock, SearchBlock, SidebarBlock, ThreeColumnBlock, TwoColumnBlock, PageHeaderBlock



@register_snippet
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField(max_length=300, blank=True)
    motto = models.CharField(max_length=80, blank=True)
    background_image = models.ForeignKey('wagtailimages.Image', null=True,
                                         blank=True,
                                         on_delete=models.SET_NULL,
                                         related_name='+')
    user_photo = models.ForeignKey('wagtailimages.Image', null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL,
                                   related_name='+')
    github = models.URLField(
        verbose_name="GitHub profile", name="githubURL", blank=True)
    linkedin = models.URLField(
        verbose_name="LinkedIn Profile", name="linkedinURL")

    panels = [
        FieldPanel('user'),
        ImageChooserPanel('user_photo'),
        ImageChooserPanel('background_image'),
        FieldPanel('linkedinURL'),
        FieldPanel('githubURL'),
        FieldPanel('biography'),
        FieldPanel('motto'), ]

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class BlogPage(RoutablePageMixin, Page):

    header = StreamField(
        [('page_header', PageHeaderBlock()), ], null=True, blank=True)
    body = StreamField([('single_column', ConstructionBlock()),
                        ('column_w_sidebar', LeftColumnWithSidebarBlock()),
                        ('two_columns', TwoColumnBlock(icon="grip")),
                        ('three_columns', ThreeColumnBlock(icon="table")
                         ), ('flex_row', InlinedItemsBlock()),
                        ('flex_row', InlinedItemsBlock()), ], null=True, blank=True)


    parent_page_types = ['home.HomePage']
    subpage_types = ['blog.PostPage','blog.LandingPage']

    content_panels = Page.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('body')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(BlogPage, self).get_context(request, *args, **kwargs)
        context['posts'] = self.posts
        context['blog_page'] = self
        context['page_author'] = self.owner
        context['search_type'] = getattr(self, 'search-type', "")
        context['search_term'] = getattr(self, 'search-term', "")
        context['menuitems'] = self.get_children().filter(
            live=True, show_in_menus=True)
        return context

    def get_posts(self):
        return PostPage.objects.descendant_of(self).live()

    @route(r'^(\d{4})/$')
    @route(r'^(\d{4})/(\d{2})/$')
    @route(r'^(\d{4})/(\d{2})/(\d{2})/$')
    def post_by_date(self, request, year, month=None, day=None, *args, **kwargs):
        self.posts = self.get_posts().filter(date__year=year)
        self.search_type = 'date'
        self.search_term = year
        if month:
            self.posts = self.posts.filter(date__month=month)
            df = DateFormat(date(int(year), int(month), 1))
            self.search_term = df.format('F Y')
        if day:
            self.posts = self.posts.filter(date__day=day)
            self.search_term = date_format(
                date(int(year), int(month), int(day)))
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^(\d{4})/(\d{2})/(\d{2})/(.+)/$')
    def post_by_date_slug(self, request, year, month, day, slug, *args, **kwargs):
        post_page = self.get_posts().filter(slug=slug).first()
        if not post_page:
            raise Http404
        return Page.serve(post_page, request, *args, **kwargs)

    @route(r'^tag/(?P<tag>[-\w]+)/$')
    def post_by_tag(self, request, tag, *args, **kwargs):
        self.search_type = 'tag'
        self.search_term = tag
        self.posts = self.get_posts().filter(tags__slug=tag)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^category/(?P<category>[-\w]+)/$')
    def post_by_category(self, request, category, *args, **kwargs):
        self.search_type = 'category'
        self.search_term = category
        self.posts = self.get_posts().filter(categories__slug=category)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^$')
    def post_list(self, request, *args, **kwargs):
        self.posts = self.get_posts()
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^search/$')
    def blog_search(self, request, *args, **kwargs):
        search_query = request.GET.get('q', None)
        self.posts = self.get_posts()
        if search_query:
            self.posts = self.posts.filter(body__contains=search_query)
            self.search_term = search_query
            self.search_type = 'search'
        return Page.serve(self, request, *args, **kwargs)


class PostPage(Page):
    date = models.DateTimeField(
        verbose_name="Post date", default=datetime.datetime.today)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    tags = ClusterTaggableManager(through='blog.BlogPageTag', blank=True)
    header = StreamField(
        [('page_header', PageHeaderBlock()), ], null=True, blank=True)
    body = StreamField([('single_column', ConstructionBlock()),
                        ('column_w_sidebar', LeftColumnWithSidebarBlock()),
                        ('two_columns', TwoColumnBlock(icon="grip")),
                        ('three_columns', ThreeColumnBlock(icon="table")),
                        ('flex_row', InlinedItemsBlock()), ], null=True, blank=True)

    parent_page_types = ['blog.BlogPage']

    content_panels = Page.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('body'),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        FieldPanel('tags'),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('date'),
    ]

    @property
    def blog_page(self):
        return self.get_parent().specific

    def get_context(self, request, *args, **kwargs):
        context = super(PostPage, self).get_context(request, *args, **kwargs)
        context['blog_page'] = self.blog_page
        context['post'] = self
        context['page_author'] = self.owner
        return context


class LandingPage(Page):

    background = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    body = StreamField([
        ('header', PageHeadingBlock()),
        ('description', blocks.CharBlock(
            required=False, icon="text-full", label="sub-title")),
        ('single_column', ConstructionBlock()),
        ('two_columns', TwoColumnBlock()),
        ('column_w_sidebar', LeftColumnWithSidebarBlock()),
        ('flex_row', InlinedItemsBlock()),
    ], null=True, blank=True)

    # Parent page / subpage type rules

    parent_page_types = ['home.HomePage','blog.LandingPage']
    subpage_types = ['blog.LandingPage']

    content_panels = Page.content_panels + [
        ImageChooserPanel('background'),
        StreamFieldPanel('body'),
    ]

    @property
    def get_blog_pages(self):
        return BlogPage.objects.sibling_of(self).live()

    @property
    def blog_page(self):
        self.blog_pages = self.get_blog_pages
        return self.blog_pages.first()


    def get_context(self, request, *args, **kwargs):
        context = super(LandingPage, self).get_context(
            request, *args, **kwargs)
        context['page_author'] = self.owner
        context['blog_page'] = self.blog_page
        return context


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('PostPage', related_name='post_tags')


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='custom_form_fields')


class FormPage(AbstractEmailForm):
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        InlinePanel('custom_form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col"),
                FieldPanel('to_address', classname="col"),
            ]),
            FieldPanel('subject'),
        ], "Email Notification Config"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(FormPage, self).get_context(request, *args, **kwargs)
        context['blog_page'] = self.blog_page
        return context

    def get_form_fields(self):
        return self.custom_form_fields.all()

    @property
    def blog_page(self):
        return self.get_parent().specific
