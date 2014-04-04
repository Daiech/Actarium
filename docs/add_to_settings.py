AUTHENTICATION_BACKENDS = (
'apps.account.backends.EmailOrUsernameModelBackend',
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
    'apps.website.context_processors.gloval_vars_url',
    'apps.website.context_processors.is_debug',
    'apps.groups_app.context_processors.get_groups',
)

ALLOWED_HOSTS = []

# add to
MIDDLEWARE_CLASSES = (
    'django.middleware.locale.LocaleMiddleware',
)
# add to
INSTALLED_APPS = (
    'apps.groups_app',
    'apps.account',
    'apps.actions_log',
    'apps.website',
    'apps.emailmodule',
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
