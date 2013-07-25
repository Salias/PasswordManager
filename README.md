## NOTE

Adaptation to Django 1.5 and enhancement from [vmalaga/PasswordManager](http://github.com/vmalaga/PasswordManager) repository

Password Manager 
====================

## Description

Password manager aims to be a simple but efective password database, but not
a sharing password application, only for a reduced number of sysadmin or developers.

My work as sysadmin, require to save a lot of passwords for installed applications
from 100 to more of 1000. Since today i was using the tool named gallinero, from that
Password Manager is based

Now I have the challenge of migrating this application to django, plus add some functionality
like send the required password the any email address

## FEATURES:

 * Search for metadata
 * Password is only viewed if you click on the password field, if not, it is hidden
 * passwords are encripted on the database based on django.core.signing
 * filters on right size django bar, date, uploader and TOP LOGINS with facets for logins with at least 3 logins
 
## REQUIREMENTS:
 * Django 1.5

## HOWTO

### DATABASE
Settings.py is configured to use SQLite3 database. If you want to use another RDBMS just change settings.py configuration
and create corresponding database name, user, password and grant access.

For example, in MYSQL case:

~~~
mysql> create database passmanager;
mysql> grant all privileges on passmanager.* to passmanager@localhost identified by 'passmanager';
~~~

See [django docs](https://docs.djangoproject.com/en/dev/ref/databases/) form more details.

~~~
$ ./manage.py syncdb
Creating tables ...
Creating table auth_permission
Creating table auth_group_permissions
Creating table auth_group
Creating table auth_user_user_permissions
Creating table auth_user_groups
Creating table auth_user
Creating table django_content_type
Creating table django_session
Creating table django_admin_log
Creating table passManager_passdb

You just installed Django's auth system, which means you don't have any superusers defined.
Would you like to create one now? (yes/no): yes
Username (leave blank to use 'vmalaga'): 
E-mail address: vmalaga
Password: 
Password (again): 
Superuser created successfully.
Installing custom SQL ...
Installing indexes ...
Installed 0 object(s) from 0 fixture(s)
~~~

### STATICS

for production enviroments with apache or other webserver remember collectstatics

~~~
$ ./manage.py collectstatic
~~~
