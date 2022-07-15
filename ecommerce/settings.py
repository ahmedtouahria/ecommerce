import os
from pathlib import Path
from decouple import  config
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-!y(2&*e_z+i+2h7_a)9)frlb^*^bun5$adalf0pp938+zd8wv1'
SECRET_KEY = config('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG')

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
      'allauth.socialaccount.providers.google', 
       'allauth.socialaccount.providers.facebook',
     'social_django',
    'rest_framework',
    'admin_interface', 
    'colorfield', 
    'django.contrib.admin',
    'constance',
    'constance.backends.database',
    'shopping',

]
CONSTANCE_ADDITIONAL_FIELDS = {
    'image_field': ['django.forms.ImageField', {}]
}
CONSTANCE_CONFIG = {
    'LOGO': ("logo.png", 'Logo du site Web',"image_field"),
    'ID_API_YALIDIN': ("", 'id de votre compte yalidin'), 
   'TOKEN_API_YALIDIN': ("", 'token de votre compte yalidin'),
   'BASE_URL_YALIDIN': ("https://api.yalidine.app/v1/", 'token de votre compte yalidin'), 

}
SESSION_COOKIE_AGE=60*60*24
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
     'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',  # <-- Here

]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',  # <-- Here
                'social_django.context_processors.login_redirect',
                
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'
AUTH_USER_MODEL='shopping.Customer'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
from dj_database_url import parse as dburl

default_dburl = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
DATABASES = {
                'default': config('DATABASE_URL', default=default_dburl, cast=dburl),
            }

""" DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'ecommerce',
    }
}
 """
# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
STATIC_ROOT=os.path.join(BASE_DIR,'static')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'ecommerce/static')]
MEDIA_ROOT = os.path.join(BASE_DIR, '') # 'data' is my media folder
MEDIA_URL = '/media/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
     'allauth.account.auth_backends.AuthenticationBackend',
)
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
SOCIAL_AUTH_FACEBOOK_KEY = '555839889591329'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = 'fc9452a738571beab5e75bf550c8d4a8'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '29609871729-p38280llfq9r2h8jq7jnsrqninstrmg2.apps.googleusercontent.com'  # App ID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'
SITE_ID = 1
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '29609871729-p38280llfq9r2h8jq7jnsrqninstrmg2.apps.googleusercontent.com',
            'secret': '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',
            'key': '',
            
        },
                'SCOPE': [
            'profile',
            'email',
        ],
    }
}
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
SOCIALACCOUNT_LOGIN_ON_GET=True
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'index'