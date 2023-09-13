from .base import *


# Longer life for access token for comfort in testing
SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(days=1)


# Add to Installed_Apps
# INSTALLED_APPS.append("debug_toolbar",)

MIDDLEWARE = [

    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Debug toolbar
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [

    "127.0.0.1",
    
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Make sure that BASE_DIR is defined somewhere at the top
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Specify the URL prefix for serving media files
MEDIA_URL = '/media/'

# Specify the filesystem path where uploaded media files will be stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')