"""
Django settings for core project.
"""

import os # IMPORTAR ACCESO AL SISTEMA DE ARCHIVOS PARA OLLAMA_CONFIG

from decouple import config, Csv # IMPORTAR DECORADORES PARA LEER VARIABLES DE ENTORNO
from pathlib import Path # IMPORTAR Path PARA MANEJO DE RUTAS DE ARCHIVOS
from datetime import timedelta # IMPORTAR timedelta PARA CONFIGURACIÓN DE JWT

BASE_DIR = Path(__file__).resolve().parent.parent # RUTA BASE DEL PROYECTO (DIRECTORIO PRINCIPAL)


# ==========================================================
# GENERAL
# ==========================================================

# OBLIGATORIA, sin valor por defecto. Asegúrate de definirla en tu .env o en las variables de entorno del sistema.
SECRET_KEY = config('SECRET_KEY') 

# DEBUG por defecto es False para seguridad. En desarrollo, define DEBUG=True en tu .env.
DEBUG = config('DEBUG', default=False, cast=bool) 

# ALLOWED_HOSTS por defecto es '*', lo cual no es seguro para producción. Asegúrate de definir hosts específicos en tu .env para producción, por ejemplo: ALLOWED_HOSTS=example.com,www.example.com
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv(), default='*')


# ==========================================================
# AUTH USER MODEL
# ==========================================================

# DEFINIR MODELO DE USUARIO PERSONALIZADO
AUTH_USER_MODEL = 'users.User'


# ==========================================================
# INSTALLED APPS
# ==========================================================

INSTALLED_APPS = [

    # APPS DE DJANGO
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # APPS DE TERCEROS PARA FUNCIONALIDADES COMUNES
    'rest_framework', # FRAMEWORK PARA CONSTRUIR APIs REST
    'rest_framework_simplejwt.token_blacklist', # PARA BLACKLIST DE TOKENS JWT
    'storages', # PARA INTEGRACIÓN CON AWS S3 (OPCIONAL)
    'corsheaders', # PARA MANEJAR CORS EN LA API HACIA EL FRONTEND
    'django_filters', # PARA FILTRADO AVANZADO EN DRF Y PAGINACIÓN
    'drf_spectacular', # PARA DOCUMENTACIÓN AUTOMÁTICA DE LA API (OpenAPI/Swagger)
    'django_celery_results', # PARA GUARDAR RESULTADOS DE TAREAS ASÍNCRONAS DE CELERY EN LA BASE DE DATOS

    'alertas.apps.AlertasConfig', # APLICACIÓN PARA MANEJO DE ALERTAS
    'aulas.apps.AulasConfig', # APLICACIÓN PARA MANEJO DE AULAS
    'bhorario.apps.BhorarioConfig', # APLICACIÓN PARA MANEJO DE HORARIOS
    'competencia.apps.CompetenciaConfig', # APLICACIÓN PARA MANEJO DE COMPETENCIAS
    'docentes.apps.DocentesConfig', # APLICACIÓN PARA MANEJO DE DOCENTES
    'ficha.apps.FichaConfig', # APLICACIÓN PARA MANEJO DE FICHAS
    'programa.apps.ProgramaConfig', # APLICACIÓN PARA MANEJO DE PROGRAMAS
    'users.apps.UsersConfig', # APLICACIÓN PARA MANEJO DE USUARIOS Y AUTENTICACIÓN
    'planificacion.apps.PlanificacionConfig', # APLICACIÓN PARA MANEJO DE PLANIFICACIÓN
    'reportes.apps.ReportesConfig', # APLICACIÓN PARA MANEJO DE REPORTES
    'notificaciones.apps.NotificacionesConfig',  # APLICACIÓN PARA MANEJO DE NOTIFICACIONES
    'exportacion.apps.ExportacionConfig',        # APLICACIÓN PARA MANEJO DE EXPORTACIÓN DE DATOS
    'analitica.apps.AnaliticaConfig', # APLICACIÓN PARA MANEJO DE ANALÍTICA Y DASHBOARDS
    'channels',
    
]


# ==========================================================
# MIDDLEWARE
# ==========================================================

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'core.middleware.audit_middleware.AuditMiddleware',
    'core.middleware.rate_limit_middleware.RolBasedRateLimitMiddleware',
    'core.middleware.cache_headers_middleware.ETagMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ==========================================================
# URLS / WSGI
# ==========================================================

ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'


# ==========================================================
# TEMPLATES
# ==========================================================

# CONFIGURACIÓN DE TEMPLATES DE DJANGO, NECESARIA PARA EL ADMIN Y OTRAS FUNCIONALIDADES QUE USEN RENDERIZADO DE TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ==========================================================
# DATABASE
# PostgreSQL si DB_NAME está definido, SQLite como fallback
# ==========================================================

# DB_NAME se lee del .env. Si no está definido, se usará SQLite por defecto para facilitar el desarrollo local sin necesidad de configurar una base de datos externa.
DB_NAME = config('DB_NAME', default=None)

if DB_NAME:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': DB_NAME,
            'USER': config('DB_USER', default=''),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }
else:
    # Si DB_NAME no está definido, usar SQLite por defecto. Esto es útil para desarrollo local sin necesidad de configurar PostgreSQL.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ==========================================================
# AUTENTICACIÓN JWT
# ==========================================================

REST_FRAMEWORK = {

    # CONFIGURACIÓN DE DRF PARA USAR JWT COMO MÉTODO DE AUTENTICACIÓN POR DEFECTO
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    # PERMISOS POR DEFECTO: EN DESARROLLO SE PERMITE CUALQUIER ACCESO PARA FACILITAR LAS PRUEBAS. EN PRODUCCIÓN, DEFINIR PERMISOS MÁS RESTRICTIVOS EN CADA VISTA O USAR UN PERMISO GLOBAL MÁS SEGURO.
    'DEFAULT_PERMISSION_CLASSES': (
    'rest_framework.permissions.AllowAny',
    ),

    # CONFIGURACIÓN DE FILTRADO Y DOCUMENTACIÓN
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],

    # CONFIGURACIÓN DE PAGINACIÓN POR DEFECTO
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    # CONFIGURACIÓN DE PAGINACIÓN POR DEFECTO: USAR PAGINACIÓN POR NÚMERO DE PÁGINA CON UN TAMAÑO DE PÁGINA DE 20 ELEMENTOS
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# CONFIGURACIÓN DE SIMPLE JWT PARA CONTROLAR LA DURACIÓN DE LOS TOKENS, EL TIPO DE AUTORIZACIÓN EN LOS HEADERS, Y LA ROTACIÓN DE TOKENS PARA MEJOR SEGURIDAD
SIMPLE_JWT = {
    # DURACIÓN DEL TOKEN DE ACCESO: 15 MINUTOS, LO CUAL ES UNA BUENA PRÁCTICA PARA REDUCIR EL RIESGO EN CASO DE QUE UN TOKEN SEA COMPROMETIDO. LOS USUARIOS PUEDEN OBTENER UN NUEVO TOKEN DE ACCESO USANDO EL TOKEN DE REFRESCO ANTES DE QUE EXPIRE
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),

    # DURACIÓN DEL TOKEN DE REFRESCO: 7 DÍAS, LO CUAL PERMITE A LOS USUARIOS MANTENER SU SESIÓN ACTIVA SIN NECESIDAD DE REAUTENTICARSE FRECUENTEMENTE, PERO TAMBIÉN LIMITA EL TIEMPO EN QUE UN TOKEN COMPROMETIDO PUEDE SER USADO
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),

    # TIPO DE AUTORIZACIÓN EN LOS HEADERS: USAR 'Bearer' ES UNA CONVENCIÓN COMÚN PARA TOKENS JWT, LO QUE HACE QUE SEA CLARO QUE SE ESTÁ USANDO UN TOKEN
    'AUTH_HEADER_TYPES': ('Bearer',),

    # HABILITAR LA ROTACIÓN DE TOKENS DE REFRESCO: CADA VEZ QUE SE USA UN TOKEN DE REFRESCO PARA OBTENER UN NUEVO TOKEN DE ACCESO, SE GENERA UN NUEVO TOKEN DE REFRESCO Y EL ANTERIOR SE INVALIDA. ESTO MEJORA LA SEGURIDAD AL REDUCIR EL RIESGO DE USO INDEBIDO DE TOKENS DE REFRESCO COMPROMETIDOS
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}


# ==========================================================
# CORS / CSRF
# ==========================================================

# EL .ENV DEBE DEFINIR CORS_ALLOW_ALL=true PARA PERMITIR TODAS LAS ORÍGENES, O CORS_ALLOW_ALL=false Y CORS_ALLOWED_ORIGINS=ORIGEN1,ORIGEN2 PARA ESPECIFICAR LOS ORÍGENES PERMITIDOS. SI CORS_ALLOW_ALL=true, SE IGNORAN LOS VALORES DE CORS_ALLOWED_ORIGINS Y SE PERMITEN TODAS LAS SOLICITUDES DE CUALQUIER ORIGEN, LO CUAL NO ES RECOMENDADO PARA PRODUCCIÓN POR RAZONES DE SEGURIDAD.
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL', cast=bool, default=False)

# SI CORS_ALLOW_ALL_ORIGINS ES FALSO, SE LEEN LOS ORÍGENES PERMITIDOS DE CORS_ALLOWED_ORIGINS, QUE DEBE SER UNA LISTA SEPARADA POR COMAS DE ORÍGENES VÁLIDOS (POR EJEMPLO: CORS_ALLOWED_ORIGINS=http://localhost:3000,https://miapp.com). SI CORS_ALLOW_ALL_ORIGINS ES VERDADERO, SE PERMITEN TODAS LAS ORÍGENES Y ESTE VALOR SE IGNORA.
if not CORS_ALLOW_ALL_ORIGINS:
    CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', cast=Csv(), default='')

# CORS_ALLOW_CREDENTIALS DEBE SER TRUE SI EL FRONTEND NECESITA ENVIAR COOKIES O CABECERAS DE AUTENTICACIÓN CON LAS SOLICITUDES CORS. ESTO ES COMÚN SI EL FRONTEND Y EL BACKEND ESTÁN EN DOMINIOS DIFERENTES Y SE NECESITA MANTENER LA SESIÓN DEL USUARIO. SI NO SE REQUIERE, ES MEJOR DEJARLO EN FALSE POR RAZONES DE SEGURIDAD.
CORS_ALLOW_CREDENTIALS = config('CORS_ALLOW_CREDENTIALS', cast=bool, default=True)

# CSRF_TRUSTED_ORIGINS DEBE SER UNA LISTA SEPARADA POR COMAS DE ORÍGENES EN LOS QUE SE CONFÍA PARA SOLICITUDES CSRF. ESTO ES IMPORTANTE SI EL FRONTEND ESTÁ EN UN DOMINIO DIFERENTE AL BACKEND, YA QUE EL NAVEGADOR SOLO INCLUYE TOKENS CSRF EN SOLICITUDES QUE SE ORIGINAN DESDE ORÍGENES DE CONFIANZA. SI NO SE CONFIGURA CORRECTAMENTE, LOS USUARIOS PUEDEN EXPERIMENTAR ERRORES DE CSRF AL INTENTAR AUTENTICARSE O REALIZAR ACCIONES PROTEGIDAS DESDE EL FRONTEND.
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', cast=Csv(), default='')


# ==========================================================
# EMAIL
# ==========================================================

# CONFIGURACIÓN DE EMAIL PARA USAR EN FUNCIONALIDADES COMO RESETEO DE CONTRASEÑA. POR DEFECTO, SE USA EL BACKEND DE CONSOLA DE DJANGO, QUE IMPRIME LOS EMAILS EN LA CONSOLA EN LUGAR DE ENVIARLOS REALMENTE. PARA PRODUCCIÓN, CONFIGURA UN BACKEND DE EMAIL REAL COMO SMTP Y PROPORCIONA LAS CREDENCIALES NECESARIAS EN EL .ENV.
EMAIL_BACKEND = config(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend',
)

# SI SE USA SMTP, SE REQUIEREN LAS SIGUIENTES CONFIGURACIONES. ASEGÚRATE DE PROPORCIONAR LOS VALORES CORRECTOS EN TU .ENV PARA QUE EL ENVÍO DE EMAILS FUNCIONE CORRECTAMENTE EN PRODUCCIÓN.
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')

# EL PUERTO POR DEFECTO PARA SMTP CON TLS ES 587, QUE ES UNA CONFIGURACIÓN COMÚN PARA SERVIDORES DE EMAIL. SI TU PROVEEDOR DE EMAIL UTILIZA UN PUERTO DIFERENTE, ASEGÚRATE DE CONFIGURARLO CORRECTAMENTE EN TU .ENV.
EMAIL_PORT = config('EMAIL_PORT', cast=int, default=587)

# TLS ES UNA PRÁCTICA RECOMENDADA PARA ENCRIPTAR LA CONEXIÓN ENTRE TU APLICACIÓN Y EL SERVIDOR DE EMAIL, PROTEGIENDO LAS CREDENCIALES Y EL CONTENIDO DE LOS EMAILS DURANTE LA TRANSMISIÓN. SI TU SERVIDOR DE EMAIL REQUIERE TLS, ASEGÚRATE DE CONFIGURARLO COMO TRUE EN TU .ENV.
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=True)

# SI TU SERVIDOR DE EMAIL REQUIERE SSL EN LUGAR DE TLS, CONFIGURA EMAIL_USE_SSL COMO TRUE Y AJUSTA EL PUERTO POR DEFECTO A 465, QUE ES COMÚN PARA SMTP CON SSL. NO DEBES USAR TLS Y SSL AL MISMO TIEMPO; ELIGE EL MÉTODO DE SEGURIDAD QUE REQUIERA TU PROVEEDOR DE EMAIL.
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')

# LA CONTRASEÑA DEL SERVIDOR DE EMAIL ES SENSIBLE Y NO DEBE INCLUIRSE DIRECTAMENTE EN EL CÓDIG FUENTE. ASEGÚRATE DE DEFINIR EMAIL_HOST_PASSWORD EN TU .ENV O EN LAS VARIABLES DE ENTORNO DEL SISTEMA PARA QUE EL ENVÍO DE EMAILS FUNCIONE CORRECTAMENTE EN PRODUCCIÓN.
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# EL EMAIL DE ORIGEN POR DEFECTO PARA LOS EMAILS ENVIADOS DESDE LA APLICACIÓN. ASEGÚRATE DE CONFIGURARLO CORRECTAMENTE EN TU .ENV, YA QUE ALGUNOS SERVIDORES DE EMAIL REQUIEREN QUE ESTE EMAIL COINCIDA CON EL USUARIO AUTENTICADO (EMAIL_HOST_USER) PARA PERMITIR EL ENVÍO DE EMAILS.
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@tudominio.com')

# URL base del frontend — usada en emails de reset de contraseña
FRONTEND_URL = config('FRONTEND_URL', default='http://localhost:3000')


# ==========================================================
# STATIC & MEDIA
# ==========================================================

# CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS Y MEDIA. POR DEFECTO, SE GUARDAN LOCALMENTE EN EL SISTEMA DE ARCHIVOS DEL SERVIDOR, PERO SI USE_S3 ES TRUE, SE CONFIGURARÁN PARA USAR AWS S3 COMO ALMACENAMIENTO DE ARCHIVOS ESTÁTICOS Y MEDIA. ASEGÚRATE DE CONFIGURAR LAS CREDENCIALES DE AWS Y LOS NOMBRES DE LOS BUCKETS EN TU .ENV SI DECIDES USAR S3.
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'


# SI USE_S3 ES TRUE, SE CONFIGURARÁN LAS VARIABLES NECESARIAS PARA USAR AWS S3 COMO ALMACENAMIENTO DE ARCHIVOS ESTÁTICOS Y MEDIA. ASEGÚRATE DE PROPORCIONAR LAS CREDENCIALES DE AWS Y LOS NOMBRES DE LOS BUCKETS EN TU .ENV PARA QUE EL ALMACENAMIENTO EN S3 FUNCIONE CORRECTAMENTE.
USE_S3 = config('USE_S3', cast=bool, default=False)

if USE_S3:
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
    AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL', default=None)
    AWS_S3_CUSTOM_DOMAIN = config(
        'AWS_S3_CUSTOM_DOMAIN',
        default=f"{config('AWS_STORAGE_BUCKET_NAME')}.s3.amazonaws.com",
    )
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = config('AWS_DEFAULT_ACL', default=None)
    AWS_QUERYSTRING_AUTH = config('AWS_QUERYSTRING_AUTH', cast=bool, default=False)

    STATIC_LOCATION = config('STATIC_LOCATION', default='static')
    MEDIA_LOCATION = config('MEDIA_LOCATION', default='media')

    STATIC_URL = config('STATIC_URL', default=f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/')
    MEDIA_URL = config('MEDIA_URL', default=f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/')

    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
            'OPTIONS': {
                'location': MEDIA_LOCATION,
            },
        },
        'staticfiles': {
            'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
            'OPTIONS': {
                'location': STATIC_LOCATION,
            },
        },
    }

else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'


# ==========================================================
# PASSWORD RESET
# Conectado a PasswordReset.get_expiration_time() vía settings
# ==========================================================

# DURACIÓN DEL TOKEN DE RESETEO DE CONTRASEÑA EN MINUTOS. SE CALCULA COMO EL NÚMERO DE HORAS DEFINIDO EN PASSWORD_RESET_EXPIRY_HOURS MULTIPLICADO POR 60. POR DEFECTO, SE ESTABLECE EN 120 MINUTOS (2 HORAS), LO CUAL ES UNA DURACIÓN RAZONABLE PARA PERMITIR A LOS USUARIOS COMPLETAR EL PROCESO DE RESETEO DE CONTRASEÑA SIN QUE EL TOKEN EXPIRE DEMASIADO RÁPIDO, PERO TAMBIÉN LIMITA EL TIEMPO EN QUE UN TOKEN COMPROMETIDO PUEDE SER USADO.
PASSWORD_RESET_EXPIRY_MINUTES = config('PASSWORD_RESET_EXPIRY_HOURS', cast=int, default=2) * 60


# ==========================================================
# PASSWORD VALIDATION
# ==========================================================

# CONFIGURACIÓN DE VALIDADORES DE CONTRASEÑA DE DJANGO PARA MEJORAR LA SEGURIDAD DE LAS CONTRASEÑAS DE LOS USUARIOS. ESTOS VALIDADORES VERIFICAN QUE LAS CONTRASEÑAS NO SEAN DEMASIADO SIMILARES A LOS ATRIBUTOS DEL USUARIO, QUE TENGAN UNA LONGITUD MÍNIMA, QUE NO SEAN CONTRASEÑAS COMUNES O NUMÉRICAS, LO CUAL AYUDA A PROTEGER LAS CUENTAS DE LOS USUARIOS CONTRA ATAQUES DE FUERZA BRUTA Y OTRAS AMENAZAS RELACIONADAS CON CONTRASEÑAS DÉBILES.
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ==========================================================
# API DOCS (drf-spectacular)
# /api/schema/         → OpenAPI JSON/YAML
# /api/schema/swagger/ → Swagger UI
# /api/schema/redoc/   → ReDoc
# ==========================================================

# CONFIGURACIÓN DE DRF SPECTACULAR PARA DOCUMENTACIÓN AUTOMÁTICA DE LA API. ESTABLECE EL TÍTULO, DESCRIPCIÓN, VERSIÓN, Y CONFIGURACIONES DE SEGURIDAD PARA LA DOCUMENTACIÓN DE LA API. TAMBIÉN INCLUYE CONFIGURACIONES PARA MEJORAR LA EXPERIENCIA DE USO DE SWAGGER UI Y REDOC, COMO MOSTRAR LA DURACIÓN DE LAS SOLICITUDES Y PERMITIR FILTRADO EN SWAGGER UI.
SPECTACULAR_SETTINGS = {
    'TITLE': config('API_TITLE', default='API'), # EL TÍTULO DE LA API SE LEERÁ DE LA VARIABLE DE ENTORNO API_TITLE, CON UN VALOR POR DEFECTO DE 'API' SI NO SE DEFINE. ASEGÚRATE DE CONFIGURAR API_TITLE EN TU .ENV PARA QUE LA DOCUMENTACIÓN DE LA API TENGA UN TÍTULO SIGNIFICATIVO.
    'DESCRIPTION': config('API_DESCRIPTION', default='Documentación de la API'), # LA DESCRIPCIÓN DE LA API SE LEERÁ DE LA VARIABLE DE ENTORNO API_DESCRIPTION, CON UN VALOR POR DEFECTO DE 'Documentación de la API' SI NO SE DEFINE. CONFIGURA API_DESCRIPTION EN TU .ENV PARA PROPORCIONAR UNA DESCRIPCIÓN CLARA Y ÚTIL DE TU API EN LA DOCUMENTACIÓN.
    'VERSION': '1.0.0', # LA VERSIÓN DE LA API SE ESTABLECE EN '1.0.0' POR DEFECTO. ACTUALIZA ESTE VALOR CADA VEZ QUE REALICES CAMBIOS SIGNIFICATIVOS EN LA API PARA MANTENER UNA BUENA GESTIÓN DE VERSIONES Y AYUDAR A LOS USUARIOS DE LA API A ENTENDER CUÁNDO HAY CAMBIOS IMPORTANTES.
    'SERVE_INCLUDE_SCHEMA': False, # NO INCLUIR EL ESQUEMA DE LA API EN LA RESPUESTA DE LA DOCUMENTACIÓN PARA REDUCIR EL TAMAÑO DE LA RESPUESTA Y MEJORAR EL RENDIMIENTO DE LA DOCUMENTACIÓN. SI NECESITAS INCLUIR EL ESQUEMA, CAMBIA ESTE VALOR A TRUE.
    'SECURITY': [{'BearerAuth': []}], # CONFIGURACIÓN DE ESQUEMA DE SEGURIDAD PARA USAR AUTENTICACIÓN BEARER CON JWT EN LA DOCUMENTACIÓN DE LA API. ESTO PERMITE A LOS USUARIOS DE LA DOCUMENTACIÓN PROBAR LOS ENDPOINTS PROTEGIDOS CON JWT AL PROPORCIONAR UN TOKEN DE ACCESO VÁLIDO.
    
    # DEFINICIÓN DEL ESQUEMA DE SEGURIDAD PARA JWT EN LA DOCUMENTACIÓN DE LA API. ESTO ES NECESARIO PARA QUE SWAGGER UI Y OTRAS HERRAMIENTAS DE DOCUMENTACIÓN PUEDAN ENTENDER CÓMO FUNCIONA LA AUTENTICACIÓN EN TU API Y PERMITIR A LOS USUARIOS PROBAR LOS ENDPOINTS PROTEGIDOS CON JWT.
    'COMPONENT_SECURITY_SCHEMES': {
        'BearerAuth': {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }
    },

    # CONFIGURACIONES DE SWAGGER UI Y REDOC PARA MEJORAR LA EXPERIENCIA DE USO DE LA DOCUMENTACIÓN. ESTAS CONFIGURACIONES PERMITEN QUE SWAGGER UI PERSISTA LA AUTORIZACIÓN ENTRE SESIONES, MUESTRE LA DURACIÓN DE LAS SOLICITUDES, Y HABILITE EL FILTRADO DE ENDPOINTS. PARA REDOC, SE CONFIGURA PARA NO OCULTAR EL BOTÓN DE DESCARGA DEL ESQUEMA.
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
        'displayRequestDuration': True,
        'filter': True,
    },

    # CONFIGURACIONES DE SWAGGER UI Y REDOC PARA MEJORAR LA EXPERIENCIA DE USO DE LA DOCUMENTACIÓN. ESTAS CONFIGURACIONES PERMITEN QUE SWAGGER UI PERSISTA LA AUTORIZACIÓN ENTRE SESIONES, MUESTRE LA DURACIÓN DE LAS SOLICITUDES, Y HABILITE EL FILTRADO DE ENDPOINTS. PARA REDOC, SE CONFIGURA PARA NO OCULTAR EL BOTÓN DE DESCARGA DEL ESQUEMA.
    'REDOC_UI_SETTINGS': {
        'hideDownloadButton': False,
    },
}

#==========================================================
# CELERY
#==========================================================

CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

from celery.schedules import crontab
CELERY_BEAT_SCHEDULE = {
    'snapshot-diario': {
        'task': 'analitica.tasks.generar_snapshot_diario',
        'schedule': crontab(hour=2, minute=0),
    },
    'limpiar-reportes': {
        'task': 'reportes.tasks.limpiar_reportes_antiguos',
        'schedule': crontab(hour=3, minute=0),
    },
}

#==========================================================
# CHANNELS
#==========================================================

ASGI_APPLICATION = 'core.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [config('REDIS_URL', default='redis://localhost:6379/0')],
        },
    },
}


#===========================================================
# OLLAMA
#===========================================================

# CONFIGURACIÓN DE OLLAMA PARA INTEGRAR MODELOS DE LENGUAJE Y EMBEDDINGS EN LA APLICACIÓN. SE CONFIGURA LA URL BASE DEL SERVICIO DE OLLAMA, LOS NOMBRES DE LOS MODELOS DE LENGUAJE Y EMBEDDINGS A USAR, Y EL DIRECTORIO DE PERSISTENCIA PARA CHROMA DB. ASEGÚRATE DE QUE EL SERVICIO DE OLLAMA ESTÉ EJECUTÁNDOSE EN LA URL CONFIGURADA Y DE QUE LOS MODELOS ESPECIFICADOS ESTÉN DISPONIBLES EN TU INSTANCIA DE OLLAMA PARA QUE LAS FUNCIONALIDADES RELACIONADAS CON LLM Y EMBEDDINGS FUNCIONEN CORRECTAMENTE.
OLLAMA_CONFIG = {
    'BASE_URL': 'http://localhost:11434',
    'LLM_MODEL': 'llama3',
    'EMBEDDING_MODEL': 'nomic-embed-text',
    'CHROMA_PERSIST_DIR': os.path.join(BASE_DIR, 'chroma_db'),
}

# ==========================================================
# INTERNACIONALIZACIÓN
# ==========================================================

LANGUAGE_CODE = config('DJANGO_LANGUAGE_CODE', default='es-co')
TIME_ZONE = config('DJANGO_TIMEZONE', default='America/Bogota')
USE_I18N = True
USE_TZ = True


# ==========================================================
# DEFAULT PRIMARY KEY
# ==========================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==========================================================
# LOGGING
# ==========================================================

LOG_LEVEL = config('LOG_LEVEL', default='INFO')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} — {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': LOG_LEVEL,
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',     # silenciar logs internos de Django en producción
            'propagate': False,
        },
        'users': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
    },
}