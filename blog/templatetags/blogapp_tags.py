# -*- coding: utf-8 -*-
import six
from ..models import BlogCategory as Category, Profile, Tag
from django.template import Library, loader, Template
from django.urls import resolve
from wagtail.core.models import Page
from blog.models import BlogPageTag




register = Library()

@register.inclusion_tag('blog/parts/author_profile.html', takes_context=True)
def author_profile(context):
    ''' Template tag outputs html content as a bootstrap4 card suitable for a sidebar or multi-column layout. It is dependant upon existence of a Profile model snippet that extends the django auth User model, and a page_author field defined in our page subclass of the wagtail Page model (or use page.owner)'''
    request = context.get('request')
    # access the foreignkey for the page's owner
    owner = context.get('page_author')
    # now get the data we want to display
    # the data is in django's User model
    # and the related snippet model called Profile (1to1 relation)
    profile = Profile.objects.get(user=owner)
    profile_photo = profile.user_photo
    background_image = profile.background_image
    motto = profile.motto
    biography = profile.biography
    githubURL = profile.githubURL
    linkedinURL = profile.linkedinURL
    email = profile.user.email
    first_name = profile.user.first_name
    last_name = profile.user.last_name

    return {
        'request': request, 'profile_photo': profile_photo, 'background_image': background_image, 'motto': motto, 'biography': biography, 'githubURL': githubURL, 'email': email, 'linkedinURL': linkedinURL, 'first_name': first_name, 'last_name': last_name, 'context': context
    }

@register.simple_tag()
def post_date_url(post, blog_page):
    post_date = post.date
    url = blog_page.url + blog_page.reverse_subpage(
        'post_by_date_slug',
        args=(
            post_date.year,
            '{0:02}'.format(post_date.month),
            '{0:02}'.format(post_date.day),
            post.slug,
        )
    )
    return url

@register.inclusion_tag('blog/parts/tags_list.html', takes_context=True)
def tags_list(context, limit=None):
    blog_page = context['blog_page']
    tags = Tag.objects.all()
    if limit:
        tags = tags[:limit]
    return {'blog_page': blog_page, 'request': context['request'], 'tags': tags}


@register.inclusion_tag('blog/parts/categories_list.html', takes_context=True)
def categories_list(context):
    blog_page = context['blog_page']
    categories = Category.objects.all()
    return {'blog_page': blog_page, 'request': context['request'], 'categories': categories}


@register.inclusion_tag('blog/parts/post_categories_list.html', takes_context=True)
def post_categories(context):
    blog_page = context['blog_page']
    post = context['post']
    post_categories = post.categories.all()
    return {'blog_page': blog_page, 'post_categories': post_categories, 'request': context['request']}


@register.inclusion_tag('blog/parts/post_tags_list.html', takes_context=True)
def post_tags_list(context):
    blog_page = context['blog_page']
    post = context['post']

    post_tags = post.tags.all()

    return {'blog_page': blog_page, 'request': context['request'], 'post_tags': post_tags}

@register.simple_tag(takes_context=True)
def canonical_url(context, post=None):
    if post and resolve(context.request.path_info).url_name == 'wagtail_serve':
        return context.request.build_absolute_uri(post_date_url(post, post.blog_page))
    return context.request.build_absolute_uri()

