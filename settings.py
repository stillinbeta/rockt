# Django settings for sibcom project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django_mongodb_engine',
        'NAME': 'rockt',
    }
}
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Toronto'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-ca'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/sib/rockt/static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/django-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+=4vi8v4jdu#@^$&i_t-u&(%m9#7s4h*th3flja00#wd0!2sq%'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'rockt.game.middleware.UsernameBalanceMiddleware',
)

ROOT_URLCONF = 'rockt.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates"
    # or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/sib/Devel/rockt/templates',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'djangorestframework',
    'django.contrib.markup',
    'rockt.game',
    'rockt.registration',
    'rockt.blog',
)

AUTH_PROFILE_MODULE = 'game.UserProfile'
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/map'

NEXTBUS_API_URL = ('http://webservices.nextbus.com/service/publicXMLFeed?' +
                   'command=vehicleLocations&a=ttc&r=%&t=0')
NEXTBUS_ROUTE_LIST = [str(num) for num in range(501, 513)]
GTFS_URL = 'http://opendata.toronto.ca/TTC/routes/OpenData_TTC_Schedules.zip'
INITIAL_BALANCE = 1000

STOP_SEARCH_LIMIT = 10
CAR_SEARCH_LIMIT = 10

RULE_CAN_BUY_CAR = 'game.rules.can_buy_car'
RULE_FIND_FARE = 'game.rules.find_fare'
RULE_GET_STREETCAR_PRICE = 'game.rules.get_streetcar_price'
