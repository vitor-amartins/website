from .base import *


SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = ['vitormartins.dev', 'www.vitormartins.dev']

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}
