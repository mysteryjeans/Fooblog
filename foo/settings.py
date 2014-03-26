# Django settings for foo project.

import os.path


from foo.blog.xmlrpc import XMLRPC_METAWEBLOG
XMLRPC_METHODS = XMLRPC_METAWEBLOG # MetaWeblog API methods

PROJECT_PATH = os.path.dirname(__file__).replace('\\', '/') # Even in windows path should be unix style

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Faraz Masood Khan', 'mk.faraz@gmail.com'),
)

MANAGERS = ADMINS

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'foodb',                      # Or path to database file if using sqlite3.
            'USER': 'devuser',                      # Not used with sqlite3.
            'PASSWORD': 'turboteen',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }
else:
    # Production database settings
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'ubuntu',                      # Or path to database file if using sqlite3.
            'USER': os.environ['DB_USERNAME'],                      # Not used with sqlite3.
            'PASSWORD': os.environ['DB_PASSWORD'],                  # Not used with sqlite3.
            'HOST': os.environ['DB_HOST'],                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': int(os.environ['DB_PORT']),                      # Set to empty string for default. Not used with sqlite3.
        }
    }

# PostgreSQL 8.4 database added.  Please make note of these credentials:

#   Root User: admin
#   Root Password: QLfG377A7r4I
#   Database Name: ubuntu

# Connection URL: postgresql://127.11.52.1:5432/
   
    
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

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
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'static', 'media') if DEBUG else os.path.join(os.environ.get('OPENSHIFT_DATA_DIR', ''), 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static') if DEBUG else os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi', 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # os.path.join(PROJECT_PATH, 'static'), # static files path
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'r74ppti1&amp;nlyh9hv^u2z%0xld0q%9lnoovii7bdu%ljmbadcba'

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
)

ROOT_URLCONF = 'foo.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'foo.wsgi.application'

TEMPLATE_DIRS = (
    # os.path.join(PROJECT_PATH, 'templates'), # static files path
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',    
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'foo.blog',
    'django_xmlrpc',
)

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

# Internal IP list
if DEBUG:
    INTERNAL_IPS = ('127.0.0.1' # for debug context processor
                    ,)

# Context processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'foo.blog.context_processors.bootstrip',
)


# fooblog settings
SITE_NAME = 'Fooblog' # Blog name
META_KEYWORDS = 'Blogging, RSS' # Default meta keywords for blog
META_DESCRIPTION = 'Everything you loved about blogging' # Blog meta description
PAGE_SIZE = 10  # Blog posts page size
