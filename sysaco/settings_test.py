"""
Settings específicos para el entorno de pruebas (CI/CD).
Usa SQLite en memoria para no requerir permiso CREATEDB en PostgreSQL.
"""
from .settings import *  # noqa: F401, F403

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SECRET_KEY = 'ci-test-secret-key-not-for-production-only'
DEBUG = True
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
