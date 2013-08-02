# [Actarium](http://actarium.com)

Actarium is built with [Python 2.7+](http://www.python.org/download/) and [Django 1.5](https://docs.djangoproject.com/en/dev/releases/1.5/)

##Install
This is the correct way to install Actarium:

1) Clone the repo on [GitHub](https://github.com/MaoAiz/Actarium)

2) [Configure your settings file](https://github.com/MaoAiz/Actarium/blob/dev/docs/add_to_settings.py)

3) Install all dependences:

###Actarium requires the next libraries

* [mongodb](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/)
* [pymongo](http://api.mongodb.org/python/current/installation.html)
* PIL [Warning! Enable support for JPG](https://jamiecurle.co.uk/blog/webfaction-installing-pil/)
* reportlab: `pip install reportlab` better from [source](http://www.reportlab.com/software/opensource/rl-toolkit/download/)
* xhtml2pdf: `pip install xhtml2pdf` better from [source](https://pypi.python.org/pypi/xhtml2pdf/)

for mongodb you should make this: `_`

###Actarium uses the next Django apps

* django-rosetta [view on GitHub](https://github.com/mbi/django-rosetta)


4) Django Internationalitation
You should have `gettext` installed on your server to use the internationalitation.
* Gettext on linux: `apt-get install gettext`
* [gettext on Windows](https://docs.djangoproject.com/en/1.5/topics/i18n/translation/#gettext-on-windows)

To compile messages:
	/Actarium/website$ `django-admin.py compilemessages`
	processing file django.po in /path_to/Actarium/website/locale/en/LC_MESSAGES

Repeat the same with all django apps that have internationalization

5) Create the required folders:
These folders need to be created manually
	
	/media
	/media/pdf
	/media/orgs_img
	/media/lastMinutes

On a terminal type: /Actarium$ `mkdir media media/pdf media/orgs_img media/lastMinutes`

6) Sync the Data Base: `python manage.py syncdb`
This will create the initial data for de db

7) Actarium is ready to run.
On development type: `python manage.py runserver`