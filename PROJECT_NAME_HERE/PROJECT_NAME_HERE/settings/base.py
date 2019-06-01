import os
import environ

# Application Version
APPLICATION_VERSION = "0.0.0"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

root = environ.Path(__file__) - 1
env = environ.Env()
environ.Env.read_env()

DEBUG = True if env('DEVELOPMENT_MODE') == 'True' else False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'crispy_forms',
    'rolepermissions',
    'snowpenguin.django.recaptcha2',
    'apps.portal',
    'apps.core',
    'apps.email',
    'apps.accounts',
    'apps.dashboard'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.accounts.middlewares.UserActivityMiddleware',
]

ROOT_URLCONF = 'PROJECT_NAME_HERE.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, '..', 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'apps.core.context_processors.site_meta_processor'
            ],
        },
    },
]

WSGI_APPLICATION = 'PROJECT_NAME_HERE.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASS'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT')
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LOGIN_REDIRECT_URL = "/dashboard"
LOGIN_URL = "/accounts/login/"

AUTH_USER_MODEL = 'accounts.User'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

ROLEPERIMISSIONS_MODULE = 'accounts.roles'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "..", "static")
]

if not os.path.exists(os.path.join(BASE_DIR, "..", "temp")):
    os.makedirs(os.path.join(BASE_DIR, "..", 'temp'))
TEMP_FILE_PATH = os.path.join(BASE_DIR, "..", 'temp')

CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672'
CELERY_TASK_ROUTES = {
    "apps.email.tasks.email_task": {'queue': 'emails'}
}


RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY')

LOGIN_AS_SESSION_FLAG = 'ouser_pk'

USE_CELERY = True if env('USE_CELERY') == 'True' else False
