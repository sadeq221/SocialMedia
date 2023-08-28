import environ
env = environ.Env()
environ.Env.read_env()

if env('DJANGO_ENV') == 'production':
    from .my_settings.settings_prod import *
else:
    from .my_settings.settings_dev import *