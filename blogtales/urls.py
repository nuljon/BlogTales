from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import (include, path,  # For django versions from 2.0 and up
                         reverse_lazy)
from filebrowser.sites import site
from taggit_templatetags2 import urls as taggit_templatetags2_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from search import views as search_views
from thewall import views as wall_views
from thewall.models import Brickmaker

from . import views

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

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('account/password_change/', auth_views.PasswordChangeView.as_view(),
             name='password_change'),
    path('account/password_change/done/', auth_views.PasswordChangeDoneView.as_view(),
             name='password_change_done'),

    path('account/password_reset/', auth_views.PasswordResetView.as_view(),
             name='password_reset'),
    path('account/password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
             name='password_reset_done'),
    path('account/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
             name='password_reset_confirm'),
    path('account/reset/done/', auth_views.PasswordResetCompleteView.as_view(),
             name='password_reset_complete'),

    path('tinymce/', include('tinymce.urls')),

    # url(r'^tags/', include('taggit_templatetags2.urls')),

    path('brickmaker/<int:pk>/update', wall_views.BrickmakerUpdate.as_view(),
         name='BrickmakerUpdate'),
    path('brickmaker/<int:pk>/', wall_views.BrickmakerDetail.as_view(), name="BrickmakerDetail"),

    path('brickmaker/', wall_views.BrickmakerDetail.as_view(), name='Brickmaker'),


    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern5 in
    # the list:
    url(r'', include(wagtail_urls), name='home')

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
]
#if settings.DEBUG:
 #   import debug_toolbar
  #  urlpatterns = [
  #     path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

   # ] + urlpatterns


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
