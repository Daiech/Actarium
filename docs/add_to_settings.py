AUTHENTICATION_BACKENDS = (
'account.backends.EmailOrUsernameModelBackend',
'django.contrib.auth.backends.ModelBackend'
)

PROJECT_PATH = os.path.realpath(".") 

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
    'website.context_processors.gloval_vars_url',
)

ALLOWED_HOSTS = []

# add to
MIDDLEWARE_CLASSES = (
    'django.middleware.locale.LocaleMiddleware',
)
# add to
INSTALLED_APPS = (
    'groups',
    'account',
    'actions_log',
    'website',
    'emailmodule',
    'rosetta'
)

ugettext = lambda s: s
LANGUAGES = (
    ('es', ugettext('Spanish')),
    ('en', ugettext('English')),
)
LOGIN_URL = "/account/login"
LOGOUT_URL = "/account/logout"
LOGIN_REDIRECT_URL = "/"
