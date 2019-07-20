from .base import *


SECRET_KEY = 'f)=23_ug)@&!x(k#e10^&n7b4*nm5b9!=a#ov$&dr^+(_c$^g1'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
