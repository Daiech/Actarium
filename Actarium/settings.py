# encoding:utf-8
import os
from django.conf import global_settings
try:
    from .local_settings import DEBUG
except ImportError:
    DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_NAME = "Actarium"
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

try:
    from .local_settings import URL_BASE
except ImportError:
    URL_BASE = "https://actarium.com"
    
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
    APPS += tuple(["django_extensions"])

try:
    from .settings_db import DATABASES
except ImportError:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3','NAME': 'actarium.sqlite','USER': '','PASSWORD': '','HOST': '','PORT': '',}}

try:
    from .settings_db import MONGODB
except:
    MONGODB = {'USER':'admin','PORT': 27017,'PASSWORD': '123456'}

ALLOWED_HOSTS = [
    ".actarium.com",
    ".actarium.com.",
    "162.243.207.189"
]

TIME_ZONE = 'America/Bogota'
LANGUAGE_CODE = 'es'

SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = tuple([os.sep.join([BASE_DIR,APP.replace('.',os.sep),'locale']) for APP in APPS])
LOCALE_PATHS += tuple([os.path.join(BASE_DIR, 'templates', 'locale')])

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

try:
    from .local_settings import STATIC_ROOT
except ImportError:
    STATIC_ROOT = "/django/actarium/static"
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR , 'static').replace('\\','/'),
)
SECRET_KEY = 'qze=v_ylqke8q1_ptjp^v-ip)pk^^6^y=6%)&amp;*l$3j#us&amp;$+go'
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates').replace('\\', '/')
)
MIDDLEWARE_CLASSES = global_settings.MIDDLEWARE_CLASSES + (
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'apps.account.middleware.MySocialAuthExceptionMiddleware',
    # 'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
)

ROOT_URLCONF = 'Actarium.urls'
WSGI_APPLICATION = 'Actarium.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
    "social.apps.django_app.default",
    "rosetta",
    "rest_framework",
    "south",
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

DEFAULT_FROM_EMAIL = 'Actarium <no-reply@daiech.com>'

TEMPLATE_CONTEXT_PROCESSORS =  global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'apps.website.context_processors.gloval_vars_url',
    'apps.website.context_processors.is_debug',
    'apps.website.context_processors.url_base',
    'actarium_apps.organizations.context_processors.my_orgs',
    'social.apps.django_app.context_processors.backends',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
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

# LOGIN_ERROR_URL = "/?error"
URL_PATH = URL_BASE
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/#welcome'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = "/account/complete-registration"
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = "/account/?msj=new-association"
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = "/account/?msg=association-deleted"
SOCIAL_AUTH_BACKEND_ERROR_URL = '/new-error-url/'
SOCIAL_AUTH_COMPLETE_URL_NAME  = '/socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = '/socialauth_associate_complete'

SOCIAL_AUTH_FORCE_POST_DISCONNECT = True
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email',]
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
GROUP_IMAGE_DEFAULT = "icons/group_default.jpg"

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


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.DjangoModelPermissions'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}





