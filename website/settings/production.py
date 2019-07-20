from .base import *


DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}

ALLOWED_HOSTS = ['vitormartins.dev', 'www.vitormartins.dev']

DEBUG = False
