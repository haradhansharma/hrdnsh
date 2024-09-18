from pathlib import Path
import environ
import os
from datetime import timedelta
# from hrdnsh.conf import LazyCurrentTemplate

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
env = environ.Env()

SECRET_KEY = env("HRDNSH_SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("No DJANGO_SECRET_KEY set for production!")

ENV_DEBUG = env("HRDNSH_DEBUG")

ENV_PRODUCTION = env("HRDNSH_PRODUCTION")

ALLOWED_HOSTS = ['*']

if ENV_DEBUG.lower() == 'true':
    DEBUG = True
    DYNAMIC_HOST_ALLOW_ALL = True
else:
    DEBUG = False
    DYNAMIC_HOST_ALLOW_ALL = False
    
ENV_PRODUCTION = env("HRDNSH_PRODUCTION")

if ENV_PRODUCTION.lower() == 'true':
    PRODUCTION = True
else:
    PRODUCTION = False
    
DYNAMIC_HOSTS_DEFAULT_HOSTS=env("HRDNSH_ALLOWED_HOST").split(',')
DYNAMIC_HOST_ALLOW_SITES=False
DYNAMIC_HOST_RESOLVER_FUNC="common.resolver.check_host"

# CORS_ALLOWED_ORIGINS = env("HRDNSH_CORS_ALLOWED_ORIGINS").split(',')


SITE_ID = 1

INSTALLED_APPS = [
    "debug_toolbar",
    'django.contrib.admin',
    'dynamic_host',
    'django_select2',
    'django_summernote',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',    
    'rest_framework',
    # 'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'drf_yasg',
    'account',
    'cms',
    'common',
    'contact',
    'hdapi',
    'django_recaptcha',  
    'project',
    'service',
    # "corsheaders",
    'guardian',
    "phonenumber_field",
    
]


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'hdapi.permissions.IsAssociatedSiteOwnerOrProfileOwner',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    
    ),
    'DEFAULT_PARSER_CLASSES': [ 
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser'
                 
    ], 
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
      
    ),
}



SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    
    'ALGORITHM': 'HS256',
   
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "hdapi.serializers.HdTokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        },
        'Basic': {
            'type': 'basic',
            'description': 'Basic HTTP Authentication'
        },
        'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header'
        }
    },
    'PERSIST_AUTH': True,
    'REFETCH_SCHEMA_WITH_AUTH': True,
    'CODEGEN_URL': 'hdapi:schema-json',
    'USE_SESSION_AUTH': False,  
    'APIS_SORTER': 'alpha',     
    'OPERATIONS_SORTER': 'alpha',
    'TAGS_SORTER': 'alpha',
    'DOC_EXPANSION': 'list',    
    'DEFAULT_MODEL_RENDERING': '',    
    'DEFAULT_MODEL_SCHEMA': '',
    'SPEC_URL' : 'hdapi:schema-json',   
    'VALIDATOR_URL': None,
    'DISPLAY_OPERATION_ID': True,
    'JSON_EDITOR': True,
    'SHOW_EXTENSIONS': True,
    'DEFAULT_EXTENSIONS': [
        'OpenAPIClientCodegen'
    ],
    # 'CONFIG_URL': 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@4.0.0/swagger-ui.css',
    
}


REDOC_SETTINGS = {
    'CODEGEN_URL': 'hdapi:schema-json',
    'SPEC_URL': 'hdapi:schema-json',
    'USE_SESSION_AUTH': False,  # Disable Django login button
    'NO_AUTO_AUTH': True,  
    'LAZY_RENDERING': True,
    # 'codegen': {
    #     'enabled': True,
    #     'languages': ['python', 'java', 'php', 'javascript'],  # Add more languages as needed
    # },
}

TEMPLATE_TAGS = ['django_summernote.templatetags.summernote']
AUTH_USER_MODEL = 'account.User'
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    'guardian.backends.ObjectPermissionBackend'
    ]

MIDDLEWARE = [ 
    
    'dynamic_host.middleware.AllowedHostMiddleWare', 
    'hrdnsh.middleware.HttpsRedirectMiddleware',   
    "corsheaders.middleware.CorsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',        
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # 'django.contrib.sites.middleware.CurrentSiteMiddleware',     
    'hrdnsh.middleware.DynamicSettingsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    'django.middleware.common.CommonMiddleware',
    
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'hrdnsh.middleware.MaintananceModeMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    
]

INTERNAL_IPS = [
  
    "127.0.0.1",
    "192.168.0.105",
    
  
]


# must be before CURRENT_TEMPLATE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',        
        'NAME': env("HRDNSH_DB_NAME"),
        'USER': env("HRDNSH_DB_USER"),
        'PASSWORD': env("HRDNSH_DB_PASSWORD"),
        'HOST': env("HRDNSH_DB_HOST"),
        'PORT': env("HRDNSH_DB_PORT"),
        'OPTIONS': {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

ROOT_URLCONF = 'hrdnsh.urls'

TEMP_DIR = 'temp_dir'

TEMP_UPLOAD_DIR = os.path.join(BASE_DIR, TEMP_DIR) 

DEFAULT_TEMPLATE = 'default'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'common.context_processor.common'
            ],
            'loaders': [
                'common.loader.CustomLoader',                 
                'django.template.loaders.app_directories.Loader', 
                # 'django.template.loaders.filesystem.Loader',              
            ],
            
        },
    },
]

WSGI_APPLICATION = 'hrdnsh.wsgi.application'


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

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


SESSION_COOKIE_NAME = 'default'

STATIC_URL = f'static/'


if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static')
    ]
       
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    
    RECAPTCHA_PUBLIC_KEY = str('6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI')
    RECAPTCHA_PRIVATE_KEY = str('6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe')
    RECAPTCHA_DOMAIN = 'www.recaptcha.net'
    SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error']
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  
    X_FRAME_OPTIONS = 'SAMEORIGIN'
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_HOST = True
    SESSION_COOKIE_HTTPONLY = True
    
    RECAPTCHA_PUBLIC_KEY = env("HRDNSH_RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = env("HRDNSH_RECAPTCHA_PRIVATE_KEY")
 
    
    # RECAPTCHA_DOMAIN = 'www.recaptcha.net'
    SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error']
    
    

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_FROM_EMAIL = env("HRDNSH_DEFAULT_FROM_EMAIL")
EMAIL_HOST = env("HRDNSH_EMAIL_HOST")
EMAIL_PORT= env("HRDNSH_EMAIL_PORT")
EMAIL_HOST_USER = env("HRDNSH_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("HRDNSH_EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
ADMIN_EMAIL = env("HRDNSH_ADMIN_EMAIL")


GPA = env("HRDNSH_GPA")

if env("HRDNSH_MAINTANANCE_MODE").lower() == 'true':
    MAINTANANCE_MODE = True
else:
    MAINTANANCE_MODE = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {  
    'default': {
        'BACKEND': 'hrdnsh.utils.CustomFileCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache'),
        'TIMEOUT': 3600,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

SELECT2_CACHE_BACKEND = 'default'


SUMMERNOTE_THEME = 'bs4'

SUMMERNOTE_CONFIG = {
    'summernote': {    
        # Change editor size
        'width': '100%',
        'height': '480',
        'codemirror': {
            'mode': 'htmlmixed',
            'lineNumbers': 'true',
            'theme': 'monokai'           
        },
    },
    'attachment_require_authentication': True,
    'css': (
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/5.29.0/theme/monokai.min.css',
    )
}



FORMATTERS = (
    {
        "verbose": {
            "format": "{levelname} {asctime} {name} {threadName} {thread} {pathname} {lineno} {funcName} {process} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {asctime} {pathname} {lineno} {message}",
            "style": "{",
        },
    },
)

HANDLERS = {
    "console_handler": {
        "class": "logging.StreamHandler",
        "formatter": "simple",
        "level": "DEBUG"
    },
    "info_handler": {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": os.path.join(BASE_DIR, 'logs/info.log' ),
        "mode": "a",
        "encoding": "utf-8",
        "formatter": "verbose",
        "level": "INFO",
        "backupCount": 5,
        "maxBytes": 1024 * 1024 * 5,  # 5 MB
    },
    "error_handler": {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": os.path.join(BASE_DIR, 'logs/error.log' ),
        "mode": "a",
        "formatter": "verbose",
        "level": "WARNING",
        "backupCount": 5,
        "maxBytes": 1024 * 1024 * 5,  # 5 MB
    },
    'hrdnsh_handler': {
        "filename": os.path.join(BASE_DIR, 'logs/debug.log' ),
        "mode": "a",
        "maxBytes": 1024 * 1024 * 5,  # 5 MB            
        'class': 'logging.handlers.RotatingFileHandler',
        "formatter": "simple",
        "encoding": "utf-8",
        "level": "DEBUG",
        "backupCount": 5,
        
    }
}

LOGGERS = (
    {
        "django": {
            "handlers": ["console_handler", "info_handler"],
            "level": "INFO",
           
        },
        "django.request": {
            "handlers": ["error_handler"],
            'level': 'INFO',             
            "propagate": True,
        },
        "django.template": {
            "handlers": ["error_handler"],
            'level': 'INFO',             
            "propagate": False,
        },
        "django.server": {
            "handlers": ["error_handler"],
            'level': 'INFO',             
            "propagate": True,
        },
        'log': {
            'handlers': ['console_handler', 'hrdnsh_handler'],
            'level': 'INFO', 
            'level': 'DEBUG',   
            "propagate": True,    
            
        },
    },
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": FORMATTERS[0],
    "handlers": HANDLERS,
    "loggers": LOGGERS[0],
}


FILE_UPLOAD_DIRECTORY_PERMISSIONS =0o777
FILE_UPLOAD_PERMISSIONS = 0o644





