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
DEBUG = False

if DEBUG:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = [".ayacollection.store"]

# Application definition

INSTALLED_APPS = [
    #'django.contrib.admin',
    'admin_ui.apps.SimpleApp',
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
    'colorfield', 
    'django.contrib.admin',
    'constance',
    'constance.backends.database',
    'shopping',
    'user_visit',

]
CONSTANCE_ADDITIONAL_FIELDS = {
    'image_field': ['django.forms.FileField', {}],
    'api_field': ['django.forms.JSONField', {
    }],
}
CONSTANCE_CONFIG = {
    'SITE_NAME': ("Aya Collection", 'le nom de site Web'),
    'SITE_URL': ("http://localhost:8000", 'le lien de site Web'),
    'SITE_MAIL': ("ahmed@gmail.com", 'mail de site Web'),
    'address': ("alger 16000 albiar", 'address'),

    'PRIMARY_COLOR': ("orange", 'le colour primaire de site Web'),
    'PROMO_LIVRASTION': (False, 'le description de livration gratuit '),
    'LOGO': ("/media/favicon.ico", 'Logo du site Web',"image_field"),
    'ID_API_YALIDIN': ("", 'id de votre compte yalidin'), 
   'TOKEN_API_YALIDIN': ("", 'token de votre compte yalidin'),
   'BASE_URL_YALIDIN': ("https://api.yalidine.app/v1/", 'token de votre compte yalidin'), 
    'Google_analytics_id': ('12345678', "l'identifiant de la vue analytics"),
    'Google_analytics_tag': ('UA-xxxxxxxx-1', "Tag de la balise"),
    'Google_analytics_credentials': ('{json}', "Votre clés d'API", 'api_field'),
    'ABOUT':('about','about your website'),
    'FACEBOOK_URL':('','URL de votre page Facebook'),
    'INSTAGRAM_URL':('','URL de votre page Instagram'),
    'WHATSAPP_NUMBER':('',' votre Numéro whatsapp'),
    'CONTACT_NUMBER':('',' votre Numéro contact'),
    'CONTACT_NUMBER2':('',' votre Numéro contact'),

}

# Admin Ui configs

SIMPLEUI_CONFIG = {
    'system_keep':False,
    'menus': [
    {
        'app': 'auth',
        'name': 'Permissions',
        'icon': 'fas fa-user-shield',
        'models': [
        {
            'name': 'Groupes',
            'icon': 'fa fa-user-lock',
            'url': 'auth/group/'
        },
        {
            'name': 'Visites',
            'icon': 'fa fa-eye',
            'url': 'user_visit/uservisit/'
        },
        ],

    },

    {
        'app': 'shopping',
        'name': 'My website',
        'icon': 'fas fa-server',
        'models':[
        {
            'name': 'Utilisateurs',
            'icon': 'fa fa-user-plus',
            'url': 'shopping/customer'
        },
    {
        'app': 'constance',
        'name': 'Configurations',
        'icon': 'fas fa-cog',
        'url': 'constance/config/'
    },
        {
            'name': 'Banner',
            'icon': 'fa fa-file-image',
            'url': 'shopping/imagebanner/'
        },
        {
            'name': 'Category',
            'icon': 'fa fa-square',
            'url': 'shopping/category'
        },
                {
            'name': 'Category Sub',
            'icon': 'fa fa-th-large',
            'url': 'shopping/categorysub'
        },
    {
            'name': 'Commandes',
            'icon': 'fa fa-shopping-cart',
            'url': 'shopping/shippingaddress'
        },
            {
            'name': 'Affaire',
            'icon': 'fa fa-bell',
            'url': 'shopping/affaire'
        },
            {
            'name': 'Produits',
            'icon': 'fa fa-female',
            'url': 'shopping/product'
        },
         {
            'name': 'Section Accueille',
            'icon': 'fa fa-tasks',
            'url': 'shopping/section'
        },
        ]
    },
    {
        'app': 'shopping',
        'name': 'My Tokens',
        'icon': 'fas fa-key',
        'models':[
        {
            'name': 'Tokens',
            'icon': 'fa fa-key',
            'url': 'socialaccount/socialapp/'
        },
        ]
    },
    ]
}

SIMPLEUI_HOME_INFO = False
SIMPLEUI_HOME_QUICK = False
SIMPLEUI_HOME_ACTION = False
SIMPLEUI_HOME_QUICK = False
SIMPLEUI_ANALYSIS = True
SIMPLEUI_HOME_TITLE = 'El Hayet'
# SIMPLEUI_LOGO = '/media/img/logo.png'
SIMPLEUI_DEFAULT_ICON = True
SIMPLEUI_DEFAULT_ICON = True
SIMPLEUI_DEFAULT_THEME = "creators.css"

SESSION_COOKIE_AGE=60*60*24
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware', 
    'user_visit.middleware.UserVisitMiddleware',
    
     # <-- Here

]

# security.W016


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
DATABASES =  {
    
        'default': config('DATABASE_URL', default=default_dburl, cast=dburl),
            } if DEBUG else {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config("DB_NAME"),
        'USER': config("DB_USER"),
        'PASSWORD': config("DB_PASSWORD"),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

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

STATIC_URL = '/static/'
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
STATIC_ROOT=os.path.join(BASE_DIR,'static/')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'root/static')]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/') # 'data' is my media folder
MEDIA_URL = '/media/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
     'allauth.account.auth_backends.AuthenticationBackend',
)
SOCIALACCOUNT_PROVIDERS = \
    {'facebook':
       {'METHOD': 'oauth2',
        'SCOPE': ['email','public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': lambda request: 'kr_KR',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.4'}}
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
SITE_ID = 'localhost'

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
SOCIALACCOUNT_LOGIN_ON_GET=True
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'index'