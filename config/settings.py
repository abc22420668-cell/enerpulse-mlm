"""
Django settings for EnerPulse MLM Platform.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-dev-key')
DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() in ('true', '1', 'yes')
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,*').split(',')

# Render.com support
RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = os.getenv(
    'CSRF_TRUSTED_ORIGINS',
    'http://localhost:8000,http://127.0.0.1:8000'
).split(',')
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')

# Application definition
INSTALLED_APPS = [
    # Django built-in
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'rosetta',
    'django_celery_beat',

    # Custom apps
    'accounts',
    'products',
    'cart',
    'orders',
    'wallet',
    'mlm',
    'payment',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Language detection middleware (replaces LocaleMiddleware)
    'i18n.middleware.LanguageDetectionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Device detection for responsive fallback
    'i18n.middleware.DeviceDetectionMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Custom context processors
                'i18n.context_processors.language_info',
                'cart.context_processors.cart_count',
                'products.context_processors.featured_products',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database — use SQLite for local dev, override with env for production
import os
DB_ENGINE = os.getenv('DB_ENGINE', 'django.db.backends.sqlite3')
if 'postgresql' in DB_ENGINE:
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': os.getenv('DB_NAME', 'olylife'),
            'USER': os.getenv('DB_USER', 'olylife'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'olylife_pass'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Custom user model
AUTH_USER_MODEL = 'accounts.User'

# Internationalization / i18n
LANGUAGE_CODE = 'zh-Hant'
TIME_ZONE = 'Asia/Taipei'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('zh-Hant', '繁體中文'),
    ('zh-Hans', '简体中文'),
    ('en', 'English'),
    ('ja', '日本語'),
    ('vi', 'Tiếng Việt'),
    ('th', 'ไทย'),
    ('id', 'Bahasa Indonesia'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Map Django language codes to locale directory names
LANGUAGE_CODE_TO_LOCALE = {
    'zh-Hant': 'zh_Hant',
    'zh-Hans': 'zh_Hans',
    'en': 'en',
    'ja': 'ja',
    'vi': 'vi',
    'th': 'th',
    'id': 'id',
}

# Country-to-language mapping for auto-detection
COUNTRY_LANGUAGE_MAP = {
    'TW': 'zh-Hant',
    'HK': 'zh-Hant',
    'MO': 'zh-Hant',
    'CN': 'zh-Hans',
    'SG': 'zh-Hans',
    'US': 'en',
    'GB': 'en',
    'AU': 'en',
    'CA': 'en',
    'JP': 'ja',
    'VN': 'vi',
    'TH': 'th',
    'ID': 'id',
    'MY': 'zh-Hans',
    'PH': 'en',
    'KR': 'en',
}

# Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Site URL (used for referral links, etc.)
SITE_URL = os.getenv('SITE_URL', 'http://localhost:8001')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Session
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Cache — fall back to local memory if Redis not available
import os as _os
_redis_url = _os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'enerpulse-cache',
    }
}

# Celery
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/1')
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Taipei'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# SimpleJWT
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# USDT Payment Settings
NOWPAYMENTS_API_KEY = os.getenv('NOWPAYMENTS_API_KEY', '')
NOWPAYMENTS_IPN_SECRET = os.getenv('NOWPAYMENTS_IPN_SECRET', '')
USDT_WALLET_ADDRESS = os.getenv('USDT_WALLET_ADDRESS', '')

# MLM Settings
MLM_PRODUCT_PV = 750  # PV per product unit
MLM_PRODUCT_PRICE_USD = 1000  # Price in USD
MLM_REFERRAL_BONUS_PCT = 0.10  # 10%
MLM_LEVEL_MATCH_PCT = 0.50  # 50%
MLM_PAIRING_BONUS_P3 = 0.11  # 11%
MLM_PAIRING_BONUS_P4 = 0.12  # 12%
MLM_PAIRING_BONUS_P5 = 0.13  # 13%
MLM_MATCHING_BONUS_GEN1 = 0.10  # 10%
MLM_MATCHING_BONUS_GEN2_6 = 0.05  # 5%
MLM_MUTUAL_AID_PCT = 0.05  # 5%
MLM_MUTUAL_AID_CAP_MULTIPLIER = 3  # 3x investment
MLM_GLOBAL_DIVIDEND_PCT = 0.05  # 5% of global sales
MLM_BONUS_WALLET_PCT = 0.80  # 80% to bonus wallet
MLM_REPURCHASE_WALLET_PCT = 0.20  # 20% to repurchase wallet
MLM_REGISTRATION_POINTS = 375  # USD shopping points on registration
MLM_REFERRAL_POINTS = 375  # USD shopping points per referral
MLM_LEVEL_MATCH_START_LEVEL = 1  # 層碰 starts from level 1
MLM_PAIRING_START_LEVEL = 4  # 對碰 starts from level 4

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'enerpulse.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'mlm': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'payment': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
