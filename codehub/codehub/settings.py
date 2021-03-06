import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',
    'articles.apps.ArticlesConfig',
    'tutorials.apps.TutorialsConfig',
    'common.apps.CommonConfig',
    'content.apps.ContentConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.postgres',
    'django.contrib.sites',
    # custom apps
    'channels',
    'rest_framework',
    'storages',
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

ROOT_URLCONF = 'codehub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE'),
        'NAME': os.environ.get('DB_NAME'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
    }
}

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

TEST_RUNNER = 'codehub.test_runner.CodehubTestRunner'

AUTH_USER_MODEL = "accounts.User"

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# custom variables go here
ARTICLE_TITLE_MIN_LENGTH = int(os.environ.get('ARTICLE_TITLE_MIN_LENGTH', 8))
ARTICLE_TITLE_MAX_LENGTH = int(os.environ.get('ARTICLE_TITLE_MAX_LENGTH', 128))
ARTICLE_CONTENT_MAX_LENGTH = int(os.environ.get('MAX_ARTICLE_LENGTH', 32768))
ARTICLE_CONTENT_MIN_LENGTH = int(os.environ.get('MIN_ARTICLE_LENGTH', 128))

TUTORIAL_TITLE_MIN_LENGTH = int(os.environ.get('TUTORIAL_TITLE_MIN_LENGTH', 8))
TUTORIAL_TITLE_MAX_LENGTH = int(os.environ.get('TUTORIAL_TITLE_MAX_LENGTH', 128))
TUTORIAL_PREVIEW_MAX_LENGTH = int(os.environ.get('TUTORIAL_PREVIEW_MAX_LENGTH', 1024))
COMMENT_MAX_LENGTH = int(os.environ.get('COMMENT_MAX_LENGTH', 4096))
SEARCH_QUERY_MAX_LENGTH = int(os.environ.get('SEARCH_QUERY_MAX_LENGTH', 64))
DEFAULT_AVATAR_URL = os.environ.get('DEFAULT_AVATAR_URL', '')
MAX_AVATAR_SIZE = os.environ.get('MAX_AVATAR_SIZE', 2097152)

# asgi setup
ASGI_APPLICATION = 'codehub.routing.application'

# static files setup
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
STATIC_URL = '/api-static/'

# aws setup
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False
# mail setup
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# host setup
HOST = os.environ.get('HOST')

# redis setup
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
SITE_ID = 1

# celery setup
CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 7200}  # 2 hours
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_IGNORE_RESULT = True
