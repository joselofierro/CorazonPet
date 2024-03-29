"""
Django settings for CorazonPet project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+x1*e*agb*v25y!w@eeft#ay)%rf2g@t6)y&3tqjvdmy5b9x%7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '192.168.10.73',
    '.elasticbeanstalk.com',
    '.corazonpet.com',
]

# Application definition
INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.historial_medicamento',
    'apps.historial_vacuna',
    'apps.mascota',
    'apps.mascota_perdida',
    'apps.raza',
    'apps.sitio_mapa',
    'apps.tipo_mascota',
    'apps.tipo_sitio',
    'apps.usuario',
    'apps.vacuna',
    'apps.aliado',
    'apps.media_mascota',
    'apps.mascota_calle',
    'apps.recordatorio',
    'apps.mascota_premium',
    'apps.custom_tag',
    'fcm_django',
    'apps.notificacion',
    'apps.departamento',
    'apps.ciudad',
    'apps.estadistica',
    'storages',
    'rest_framework',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CorazonPet.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'CorazonPet.wsgi.application'

# variable global de autentificacion por token
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'corazonpet',
            'USER': 'postgres',
            'PASSWORD': 'backend17',
            'HOST': 'localhost',
            'PORT': 5432
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'
# MEDIA_URL = '/media/'

# DONDE DJANGO BUSCAR NUESTROS ARCHIVOS (donde estaran en el proyecto)
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
# donde seran enviados los archivos estaticos que viven en la carpeta static (entorno de servidor)
STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")

# imagenes subidas por usuario en entorno del server
MEDIA_ROOT = os.path.join(BASE_DIR, "..", "www", "media/")

# S3
AWS_STORAGE_BUCKET_NAME = 'corazonpet'
AWS_ACCESS_KEY_ID = 'AKIAJ6M7ESITMZ2HV53Q'
AWS_SECRET_ACCESS_KEY = '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'

# Tell django-storages the domain to use to refer to static files.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# Tell the staticfiles app to use S3Boto3 storage when writing the collected static files (when
# you run `collectstatic`).
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

# (Firebase Cloud Messaging)
FCM_DJANGO_SETTINGS = {
    # token de la app movil en firebase
    "FCM_SERVER_KEY": "AAAAlPf3Ox8:APA91bHpafRXffnw-uIZGDPA40YDVS5WuqqvARJIiC8IeV98LxoVS-xzqrmPHRqU9NmtqOmMJl3HcEfyDS0gkdUzkKMBFSwXO6Yw7T9IYqUWUFD1BUAkpUKDmulENfKfkrbNVmH2f_dh",
    # true if you want to have only one active device per registered user at a time
    # default: False
    "ONE_DEVICE_PER_USER": True,
    # devices to which notifications cannot be sent,
    # are deleted upon receiving error response from FCM
    # default: False
    "DELETE_INACTIVE_DEVICES": False,

}

# EMAIL CONFIG
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'backend.corazonpet@gmail.com'
EMAIL_HOST_PASSWORD = 'CorazonPet2017'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
