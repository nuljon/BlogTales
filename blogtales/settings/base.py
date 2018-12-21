"""
Django settings for blogtales project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from django.conf.global_settings import INTERNAL_IPS


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'home',
    'search',
    'blog',
    'colorblock',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.routable_page',
    'wagtail.contrib.styleguide',
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.settings',
    'wagtailmenus',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtailcodeblock',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    'modelcluster',
    'taggit',
    'taggit_templatetags2',
    'treebeard',
    'threadedcomments',
    'fluent_comments',  # must be before django_comments
    'crispy_forms',
    'django_comments',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'debug_toolbar',
    'debugtools',
]


MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',

]

ROOT_URLCONF = 'blogtales.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtailmenus.context_processors.wagtailmenus',
                'django.template.context_processors.static',
            ],
            'builtins': [                                     # Add this section
                "debugtools.templatetags.debugtools_tags",   # Add this line
            ],
        },
    },
]

WSGI_APPLICATION = 'blogtales.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# Javascript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/2.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

INTERNAL_IPS = ('127.0.0.1')

# Wagtail settings
WAGTAIL_SITE_NAME = "blogtales"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://example.com'


# wagtail image processing - features rely on open cv2 nd numpy
WAGTAILIMAGES_FEATURE_DETECTION_ENABLED = True

WAGTAIL_CODE_BLOCK_LANGUAGES = (
    ('bash', 'Bash/Shell'),
    ('css', 'CSS'),
    ('diff', 'diff'),
    ('html', 'HTML'),
    ('javascript', 'Javascript'),
    ('json', 'JSON'),
    ('python', 'Python'),
    ('scss', 'SCSS'),
    ('yaml', 'YAML'),
    ('cpp', 'C++')
)

##############################  configure TAGS and TAG CLOUD

TAGGIT_CASE_INSENSITIVE = True
# tag cloud limit default is 10
TAGGIT_LIMIT = 150
#tag cloud order by default is name
TAGGIT_TAG_CLOUD_ORDER_BY = '-num_times'


####################### configure COMMENTS-FRAMEWORK  #########################

#######  fluent-comments default config values
# AKISMET_API_KEY = None
# AKISMET_BLOG_URL = None
# AKISMET_IS_TEST = False
# CRISPY_TEMPLATE_PACK = 'bootstrap'
# FLUENT_COMMENTS_REPLACE_ADMIN = True
###### #Akismet spam fighting
# FLUENT_CONTENTS_USE_AKISMET = bool(AKISMET_API_KEY)
# FLUENT_COMMENTS_AKISMET_ACTION = 'soft_delete'
###### Moderation
# FLUENT_COMMENTS_DEFAULT_MODERATOR = 'default'
# FLUENT_COMMENTS_CLOSE_AFTER_DAYS = None
# FLUENT_COMMENTS_MODERATE_BAD_WORDS = ()
# FLUENT_COMMENTS_MODERATE_AFTER_DAYS = None
# FLUENT_COMMENTS_USE_EMAIL_NOTIFICATION = True
# FLUENT_COMMENTS_MULTIPART_EMAILS = False
####### Form layouts
# FLUENT_COMMENTS_FIELD_ORDER = ()
# FLUENT_COMMENTS_EXCLUDE_FIELDS = ()
# FLUENT_COMMENTS_FORM_CLASS = None
# FLUENT_COMMENTS_FORM_CSS_CLASS = 'comments-form form-horizontal'
# FLUENT_COMMENTS_LABEL_CSS_CLASS = 'col-sm-2'
# FLUENT_COMMENTS_FIELD_CSS_CLASS = 'col-sm-10'
####### Compact style settings
# FLUENT_COMMENTS_COMPACT_FIELDS = ('name', 'email', 'url')
# FLUENT_COMMENTS_COMPACT_GRID_SIZE = 12
#FLUENT_COMMENTS_COMPACT_COLUMN_CSS_CLASS = "col-sm-{size}"
####### end fluent-comments default config values

COMMENTS_APP = 'fluent_comments'

# config fluent_comments FORM (*default)

# FLUENT_COMMENTS_FORM_CLASS = 'fluent_comments.forms.DefaultCommentForm'*
FLUENT_COMMENTS_FORM_CLASS = 'fluent_comments.forms.CompactCommentForm'
# replace the labels with placeholders
# FLUENT_COMMENTS_FORM_CLASS = 'fluent_comments.forms.CompactLabelsCommentForm'

# assign or override classes to customize styles
# FLUENT_COMMENTS_FORM_CSS_CLASS = 'comments-form form-horizontal'*
FLUENT_COMMENTS_LABEL_CSS_CLASS = 'col-sm-2'
# FLUENT_COMMENTS_FIELD_CSS_CLASS = 'col-sm-10'*

# Optional settings for the compact style:
FLUENT_COMMENTS_COMPACT_FIELDS = ('comment', 'name')
FLUENT_COMMENTS_COMPACT_GRID_SIZE = 12
FLUENT_COMMENTS_COMPACT_COLUMN_CSS_CLASS = 'col-sm-10'

# display fields to render visible in order deisired
FLUENT_COMMENTS_FIELD_ORDER = ('comment', 'name', 'email', 'url')

# alternatively, hide fields from rendeering
# FLUENT_COMMENTS_EXCLUDE_FIELDS = ('email', 'url')

# crispy forms template pack used by comments
CRISPY_TEMPLATE_PACK = 'bootstrap4'

####################### configure DJANGO SITES-FRAMEWORK - required by comments
SITE_ID = 1
