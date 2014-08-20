# This is your project's main settings file that can be committed to your
# repo. If you need to override a setting locally, use settings_local.py

from funfactory.settings_base import * # noqa

# Name of the top-level module where you put all your apps.
# If you did not install Playdoh with the funfactory installer script
# you may need to edit this value. See the docs about installing from a
# clone.
PROJECT_MODULE = 'wprevents'

# Defines the views served for root URLs.
ROOT_URLCONF = '%s.urls' % PROJECT_MODULE

INSTALLED_APPS = (['south'] +
                  list(INSTALLED_APPS) + [
                      # Application base, containing global templates.
                      '%s.base' % PROJECT_MODULE,
                      '%s.events' % PROJECT_MODULE,
                      '%s.admin' % PROJECT_MODULE,

                      'django_browserid',
                      'tastypie'])

# Note! If you intend to add `south` to INSTALLED_APPS,
# make sure it comes BEFORE `django_nose`.
# INSTALLED_APPS.remove('django_nose')
# INSTALLED_APPS.append('django_nose')


LOCALE_PATHS = (
    os.path.join(ROOT, PROJECT_MODULE, 'locale'),
)

# Because Jinja2 is the default template loader, add any non-Jinja templated
# apps here:
JINGO_EXCLUDE_APPS = (
    'admin',
    'registration',
    'browserid',
)

# BrowserID configuration
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_browserid.auth.BrowserIDBackend',
    # 'wprevents.base.auth.BrowserIDBackend',
)

SITE_URL = 'http://localhost:8000'

# Use default BrowserID verification class
BROWSERID_VERIFY_CLASS = 'django_browserid.views.Verify'

# Do not create user on login
BROWSERID_CREATE_USER = False

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/admin/events'
LOGIN_REDIRECT_URL_FAILURE = '/'

# Remove LocaleURLMiddleware since we are not localing our website
MIDDLEWARE_CLASSES = filter(
    lambda x: x != 'funfactory.middleware.LocaleURLMiddleware',
    MIDDLEWARE_CLASSES)

# TEMPLATE_CONTEXT_PROCESSORS += (
# )

# Should robots.txt deny everything or disallow a calculated list of URLs we
# don't want to be crawled?  Default is false, disallow everything.
# Also see http://www.google.com/support/webmasters/bin/answer.py?answer=93710
ENGAGE_ROBOTS = False

# Always generate a CSRF token for anonymous users.
ANON_ALWAYS = True

# Tells the extract script what files to look for L10n in and what function
# handles the extraction. The Tower library expects this.
DOMAIN_METHODS['messages'] = [
    ('%s/**.py' % PROJECT_MODULE,
        'tower.management.commands.extract.extract_tower_python'),
    ('%s/**/templates/**.html' % PROJECT_MODULE,
        'tower.management.commands.extract.extract_tower_template'),
    ('templates/**.html',
        'tower.management.commands.extract.extract_tower_template'),
]

# # Use this if you have localizable HTML files:
# DOMAIN_METHODS['lhtml'] = [
#    ('**/templates/**.lhtml',
#        'tower.management.commands.extract.extract_tower_template'),
# ]

# # Use this if you have localizable JS files:
# DOMAIN_METHODS['javascript'] = [
#    # Make sure that this won't pull in strings from external libraries you
#    # may use.
#    ('media/js/**.js', 'javascript'),
# ]


# Set ALLOWED_HOSTS based on SITE_URL.
def _allowed_hosts():
    from django.conf import settings
    from urlparse import urlparse

    host = urlparse(settings.SITE_URL).netloc  # Remove protocol and path
    host = host.rsplit(':', 1)[0]  # Remove port
    return [host]
ALLOWED_HOSTS = lazy(_allowed_hosts, list)()

LOGGING = {
    'loggers': {
        'playdoh': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'django_browserid': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}


# List of valid country codes.
def lazy_countries():
    from product_details import product_details

    try:
        return product_details.get_regions('en-US')
    except IOError:
        return {u'us': 'United States'}
COUNTRIES = lazy(lazy_countries, dict)()

# MEDIA
MEDIA_ROOT = '/tmp/upload'
MEDIA_URL = '/media/'

USE_TZ = True
TIME_ZONE = 'UTC'
