#!/bin/bash
uwsgi --socket :9010 --wsgi-file Actarium/wsgi.py -d logfile.log


