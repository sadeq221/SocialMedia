from .settings_base import *

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Make sure that BASE_DIR is defined somewhere at the top
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Specify the URL prefix for serving media files
MEDIA_URL = '/media/'

# Specify the filesystem path where uploaded media files will be stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')