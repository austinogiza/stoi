
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(&+h5h=15$-iom$h9%w5u-e7pu4#m^lyc#ib!sv6)kg66ex1=e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
        'jet.dashboard',
      'jet', ##admin dashboard
      
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
   
'core', ##main app
    "sorl.thumbnail",
    'django_filters',
       'ckeditor',
    "ckeditor_uploader",
    "django.contrib.humanize",
    'crispy_forms',
     'django.contrib.sites',
         'django_countries', 
             'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'paystack',  ##paystack app
    "taggit"
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

# paystack
# PAYSTACK_PUBLIC_KEY = "pk_live_3b7b32232d4485c95cdc0c50f83acda3b6f523b1"
# PAYSTACK_SECRET_KEY = "sk_live_1c2a919aca68e2a4fb2369cd828972d801a29d80"

PAYSTACK_PUBLIC_KEY = "pk_test_55802056c3f92e6f555a0f3cb60191e858907811"
PAYSTACK_SECRET_KEY = "sk_test_a9c9c1cd62514b84f9b709e6a2b0ced0005e445c"


ROOT_URLCONF = 'stroyal.urls'

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

JET_SIDE_MENU_COMPACT = True

WSGI_APPLICATION = 'stroyal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'stroyal',
        'USER': 'postgres',
        'HOST': 'localhost',
        'PORT': '',
        'PASSWORD': 'austinforreal'
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]


STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CKEDITOR_UPLOAD_PATH = "uploads/"

from django.contrib import messages

AUTHENTICATION_BACKENDS = [

    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


MESSAGE_TAGS = {
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger'

}

SITE_ID = 1

AUTH_USER_MODEL = 'core.CustomUser'

ACCOUNT_AUTHENTICATION_METHOD= "username_email"

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_LOGOUT_ON_GET = True

LOGIN_REDIRECT_URL = '/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

ACCOUNT_AUTHENTICATION_METHOD = "username_email"

LOGIN_REDIRECT_URL ='/'

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3

# ACCOUNT_EMAIL_REQUIRED = True

# ACCOUNT_EMAIL_VERIFICATION = "mandatory"

ACCOUNT_SESSION_REMEMBER = True


# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'janesfash@gmail.com'
EMAIL_HOST_PASSWORD = "sogie2020"


ACCOUNT_FORMS = {'signup': 'core.forms.CustomSignupForm'}

TAGGIT_CASE_INSENSITIVE = True