import os

django_env = os.environ.get('DJANGO_ENV', "local")

if django_env == 'development':
    from zapdos_api.settings.dev import *
elif django_env == 'production':
    from zapdos_api.settings.prod import *
else:
    from zapdos_api.settings.local import *