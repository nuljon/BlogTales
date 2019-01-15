from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import include, path  # For django versions from 2.0 and up
from filebrowser.sites import site
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from taggit_templatetags2 import urls as taggit_templatetags2_urls
from thewall import views as wall_views
from thewall.models import Brickmaker
from . import views


from search import views as search_views



urlpatterns = [
    path('admin/filebrowser/', site.urls),
    url(r'^django-admin/', admin.site.urls),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/$', search_views.search, name='search'),

    url(r'^comments/', include('django_comments.urls')),
    url(r'^blog/comments/', include('fluent_comments.urls')),

    path('brick/new/<int:wall_page>/', wall_views.brick_new, name='brick_new'),
    path('brick/<int:pk>/', wall_views.brick_detail, name='brick_detail'),
    path('brick/edit/<int:pk>/', wall_views.brick_edit, name='brick_edit'),

    path('signup/', views.signup, name='signup'),
  # path('secret/', views.secret_page, name='secret'),
  #  path('secret2/', views.SecretPage.as_view(), name='secret2'),
  # path('accounts/', include('django.contrib.auth.urls')),
    path('tinymce/', include('tinymce.urls')),

    # url(r'^tags/', include('taggit_templatetags2.urls')),

    path('brickmaker/new/<str:user>', wall_views.BrickmakerCreateView.as_view(),
         name='BrickmakerCreateView'),


    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls), name='home')

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
