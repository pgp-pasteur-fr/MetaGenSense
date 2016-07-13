MetaGenSense
============

   A web application framework for analysis and visualization of High throughput Sequencing metagenomic data.

Citation
--------

   Correia D, Doppelt-Azeroual O, Denis JB et al. MetaGenSense : A web application for analysis and visualization of high     throughput sequencing metagenomic data [v1; ref status: approved with reservations 2, not approved 1,     http://f1000research.com/articles/4-86/v1 ] F1000Research 2015.

Requirements
------------

- python==2.7
- Django==1.6.2
- bioblend==0.5.3

Installation
------------

1. virtualenv

    You may use virtualenv to isolate your django project workspace [virtualenv](http://www.virtualenv.org/),
   [virtualenvwrapper](http://www.doughellmann.com/projects/virtualenvwrapper/)

2. Download

    You need the *MetaGenSense* project files in your workspace:

      - cd /path/to/your/workspace
      - git clone git://github.com/pgp-pasteur-fr/MetaGenSense.git

3. Requirements installation

   $ pip install -r requirements.txt

4. Set the settings: 

   a. wsgi.py
   
     `MetaGenSense/wsgi.py` file is necessary for WSGI gateways (such as uWSGI) to run your Django application and is also
     required from Django itself. You definitely want to change `{{ project_name }}` value in this file to the name of your
     application (e.g. `metagensense.settings`).

   b. SECRET_KEY setting
   
     Create your own secret key. Open your `MetaGenSense/settings.py`, find `SECRET_KEY` line, paste your secret key.
     [SECRET_KEY](cf. https://docs.djangoproject.com/en/1.8/ref/settings/#secret-key)

   c. Paths setting
   
     Set up this paths for you personal configuration/architecture .

     Paths to access to Galaxy personal import directory form server:

         - GALAXY_SERVER_URL = http://.... #url to your Galaxy server
         - GALAXY_INPUT_DIR = 'links'      #path to put data into Galaxy with import tool
         - MGS_GALAXY_FOLDER = '/MGS' #absolute path to Galaxy library (directory inside links)
    

     Path where to store uploaded files:

         MGS_UPLOAD_FILE_DIR = os.path.join(os.path.sep,'opt','metagensense','limsfiles')

     Folder to save analyse results on the server:

         ANALYSE_FOLDER = 'analyse'

     Folder use to export big data by MetaGenSense (>2Gb)':

         WK_EXPORT_DIR = '/opt/MGS/outputs'


   d. Initialize the database
   
     First you must have an database engine instaledl on your machine, 
     Set the database engine (PostgreSQL, MySQL, etc..) in your settings files; `MetaGenSense/settings.py` at `DATABASES` 
     [DATABASES](https://docs.djangoproject.com/en/1.8/ref/settings/#databases)
     
     Create django models with the command: 
         - ./manage.py migrate`

   e. Test settings

     Starts a lightweight development Web server on the local machine. 
     By default, the server runs on port 8000 on the IP address 127.0.0.1. 
     You can pass in an IP address and port number explicitly.
         - ./manage.py runserver



