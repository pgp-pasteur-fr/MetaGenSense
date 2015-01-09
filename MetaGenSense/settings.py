# -*- coding: utf-8 -*-
"""
Django settings for MetaGenSense project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
import sys
import django.conf.global_settings as DEFAULT_SETTING


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/home"


#Workflow application use by MetaGensense
WORKWFLOW_MANAGEMENT_SYSTEM = 'Galaxy'
WK_EXPORT_DIR = '/opt/MGS/outputs/'

#Path to access to Galaxy personal import directory form server
GALAXY_SERVER_DIR ='/pasteur/projets/common/galaxy/links/'
GALAXY_SERVER_URL ='https://galaxy.web.pasteur.fr/'

#folder to save analyse on the server
ANALYSE_FOLDER= 'analyse'

#Python Path for Reusable Django Apps
sys.path.insert(0, PROJECT_PATH )

#Path to store upload file 
MGS_UPLOAD_FILE_DIR = os.path.join(os.path.sep,'opt','MetaGenSense','share_files')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$14mp59lzp!3!g)orjb*0ejnqb=gj13li9_6c$69stz*mibr*1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps on MetaGenSense
    'MetaGenSense.apps.lims',
    'MetaGenSense.apps.usermanagement',
    'MetaGenSense.apps.workflow_remote',
    'MetaGenSense.apps.analyse',  
    
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'MetaGenSense.urls'

WSGI_APPLICATION = 'MetaGenSense.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = MGS_UPLOAD_FILE_DIR
FILE_UPLOAD_PERMISSIONS= 0664

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
ADMIN_MEDIA_PREFIX = '/static/'
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (              
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'static'),
    
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTING.TEMPLATE_CONTEXT_PROCESSORS + (
    "MetaGenSense.apps.lims.context_processor.add_project",
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (                 
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_PATH + '/templates',
)


