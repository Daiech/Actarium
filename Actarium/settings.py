# encoding:utf-8
# Django settings for Actarium project.
import os.path
# try:
#     from .local_settings import DEBUG
# except Exception:
DEBUG = True
TEMPLATE_DEBUG = DEBUG
# PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
PROJECT_PATH = os.path.realpath(".")
URL_BASE = "http://actarium.com:8000"

ADMINS = (
    ('Mauricio Aizaga', 'maizaga@daiech.com'),
    ('Edwin Mesa', 'emesa@daiech.com'),
    ('Lina Aguirre', 'laguirre@daiech.com'),
)

MANAGERS = ADMINS
APPS = ['apps.groups_app','apps.account','apps.actions_log','apps.website','apps.emailmodule',
'actarium_apps.customers_services', 'actarium_apps.organizations','actarium_apps.core']

RESERVED_WORDS = ["meal", "admin", "account", "groups", "pdf", "actions", "settings", "ads", "tour", "about", "feed-back", "blog", "update", "runMongo", "actarium", "services", "i18n", "oauth", "media", "static", "rosetta"]

if DEBUG:
    APPS += ["django_extensions"]
    pass


try:
    from .settings_db import DATABASES
except ImportError:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'actarium',                      # Or path to database file if using sqlite3.
            'USER': 'root',                      # Not used with sqlite3.
            'PASSWORD': 'holamundo',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }
ALLOWED_HOSTS = ["actarium.com", ".actarium.com", "actarium.anunciosuniversitarios.com", "actarium.daiech.com", "localhost"]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Bogota'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = "" #os.path.join(os.path.dirname(os.path.dirname(__file__)) , 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(os.path.dirname(__file__)) , 'static').replace('\\','/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'qze=v_ylqke8q1_ptjp^v-ip)pk^^6^y=6%)&amp;*l$3j#us&amp;$+go'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'Actarium.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'Actarium.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates').replace('\\', '/')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    # 'social.apps.django_app.default',
    # 'rosetta',
    # 'django_extensions',
) + tuple(APPS)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#Configurando from email por defecto
DEFAULT_FROM_EMAIL = 'Actarium <no-reply@daiech.com>'

ORGS_IMG_DIR = "orgs_img/"

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    # "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
    'apps.website.context_processors.gloval_vars_url',
    'apps.website.context_processors.is_debug',
    'actarium_apps.organizations.context_processors.my_orgs',
    'social.apps.django_app.context_processors.backends',
)

AUTHENTICATION_BACKENDS = (
    # 'social.backends.google.GoogleOAuth2',
    # 'social.backends.twitter.TwitterOAuth',
    'social.backends.facebook.FacebookOAuth2',
    'apps.account.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend'
)

ugettext = lambda s: s
LANGUAGES = (
    ('es', ugettext('Spanish')),
    ('en', ugettext('English')),
)
LANGUAGES = (
    ('es', 'Spanish'),
    ('en', 'English'),
)
LOGIN_URL = "/account/login"
LOGOUT_URL = "/account/logout"
LOGIN_REDIRECT_URL = "/"

# LOGIN_ERROR_URL = "/except"
URL_PATH = URL_BASE
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/#welcome'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = "/account/complete-registration"
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = "/account/?msj=new-association"
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = "/account/?msj=association-deleted"
SOCIAL_AUTH_BACKEND_ERROR_URL = '/new-error-url/'
SOCIAL_AUTH_COMPLETE_URL_NAME  = '/socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = '/socialauth_associate_complete'

SOCIAL_AUTH_FORCE_POST_DISCONNECT = True
# SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email',]
SOCIALredirect_AUTH_UID_LENGTH = 767
SOCIAL_AUTH_UUID_LENGTH = 16
SOCIAL_AUTH_SLUGIFY_USERNAMES = True
SOCIAL_AUTH_FORCE_RANDOM_USERNAME = False

SOCIAL_AUTH_FORCE_EMAIL_VALIDATION = False
SOCIAL_AUTH_EMAIL_FORM_URL = '/signup-email'
SOCIAL_AUTH_EMAIL_FORM_HTML = 'email_signup.html'
SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION = 'apps.account.mail.send_validation'
# # SOCIAL_AUTH_EMAIL_VALIDATION_URL = reverse('email_sent')
SOCIAL_AUTH_USERNAME_FORM_URL = '/signup-username'
SOCIAL_AUTH_USERNAME_FORM_HTML = 'username_signup.html'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False


SOCIAL_AUTH_EMAIL_NOT_UNIQUE_URL = "/account/complete-registration?msj=ya-existe-ese-email"

SOCIAL_AUTH_PIPELINE = ( 
    'social.pipeline.social_auth.social_details', 
    'social.pipeline.social_auth.social_uid', 
    'social.pipeline.social_auth.auth_allowed', 
    # 'social.pipeline.social_auth.social_user', 
    'account.social_auth.social_user',
    'social.pipeline.user.get_username', 
    # 'social.pipeline.social_auth.associate_by_email', 
    # 'social.pipeline.mail.mail_validation',
    'account.social_auth.mail_unique',
    'social.pipeline.user.create_user', 
    'social.pipeline.social_auth.associate_user', 
    'social.pipeline.social_auth.load_extra_data', 
    'social.pipeline.user.user_details' 
) 

try:
    from .local_settings import *
except ImportError:
    pass

ORG_IMAGE_SIZE = ((50,50), (100,100))
ORG_IMAGE_DEFAULT = "icons/org_default.jpg"

GROUP_IMAGE_SIZE = ((50,50), (100,100))
GROUP_IMAGE_DEFAULT = "orgs_img/default.jpg"

GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

try:
    from .local_settings import EMAIL_HOST_USER
except:
    EMAIL_HOST_USER = ""
try:
    from .local_settings import EMAIL_HOST_PASSWORD
except:
    EMAIL_HOST_PASSWORD = ""


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
