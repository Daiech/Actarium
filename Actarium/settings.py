# encoding:utf-8
# Django settings for Actarium project.
import os
try:
    from .local_settings import DEBUG
except ImportError:
    print "ERROR DEBUG"
    DEBUG = True
TEMPLATE_DEBUG = DEBUG
PROJECT_PATH = os.path.realpath(".")
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_NAME = "Actarium"
try:
    from .local_settings import URL_BASE
except ImportError:
    URL_BASE = "http://actarium.com"
    
ADMINS = (
    ('Mauricio Aizaga', 'maizaga@daiech.com'),
    ('Edwin Mesa', 'emesa@daiech.com'),
    ('Lina Aguirre', 'laguirre@daiech.com'),
)

MANAGERS = ADMINS

APPS = tuple()
folder_apps = ["apps", "actarium_apps"]

for app in folder_apps:
    APPS += tuple([app+"."+x for x in os.listdir(os.sep.join([BASE_DIR,app])) if os.path.isdir(os.sep.join([BASE_DIR,app,x]))])

RESERVED_WORDS = ["meal", "admin", "account", "groups", "pdf", "actions", "settings", "ads", "tour", "about", "feed-back", "blog", "update", "runMongo", "actarium", "services", "i18n", "oauth", "media", "static", "rosetta", "pricing"]

if DEBUG:
    APPS += tuple(["django_extensions", "social.apps.django_app.default"])
print APPS
try:
    from .settings_db import DATABASES
except ImportError:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'actarium.sqlite',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }

try:
    from .settings_db import MONGODB
except:
    MONGODB = {
        'USER':'admin',
        'PORT': 27017,
        'PASSWORD': '123456'
    }
    
ALLOWED_HOSTS = ["*"]

TIME_ZONE = 'America/Bogota'

LANGUAGE_CODE = 'es'

SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = "" #os.path.join(BASE_DIR , 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR , 'static').replace('\\','/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

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
    os.path.join(BASE_DIR, 'templates').replace('\\', '/')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
) + APPS

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
    'apps.website.context_processors.url_base',
    'actarium_apps.organizations.context_processors.my_orgs',
    'social.apps.django_app.context_processors.backends',
)

AUTHENTICATION_BACKENDS = (
    # 'social.backends.google.GoogleOAuth2',
    # 'social.backends.twitter.TwitterOAuth',
    # 'social.backends.facebook.FacebookOAuth2',
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
    'apps.account.social_auth.social_user',
    'social.pipeline.user.get_username', 
    # 'social.pipeline.social_auth.associate_by_email', 
    # 'social.pipeline.mail.mail_validation',
    'apps.account.social_auth.mail_unique',
    'social.pipeline.user.create_user', 
    'social.pipeline.social_auth.associate_user', 
    'social.pipeline.social_auth.load_extra_data', 
    'social.pipeline.user.user_details' 
) 

ORG_IMAGE_SIZE = ((50,50), (100,100))
ORG_IMAGE_DEFAULT = "icons/org_default.jpg"

GROUP_IMAGE_SIZE = ((50,50), (100,100))
GROUP_IMAGE_DEFAULT = "orgs_img/default.jpg"

GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

############## EMAIL CONFIGURATION #################
try:
    from .local_settings import EMAIL_HOST_USER
except:
    EMAIL_HOST_USER = "no-reply@daiech.com"
try:
    from .local_settings import EMAIL_HOST_PASSWORD
except:
    EMAIL_HOST_PASSWORD = ""

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL="Actarium <{email}>".format(email=EMAIL_HOST_USER)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_SUBJECT_PREFIX = "[Actarium] "
############## EMAIL CONFIGURATION #################

try:
    from .local_settings import *
except ImportError:
    pass
