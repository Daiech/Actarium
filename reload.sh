#!/bin/bash
ps -Af | grep uwsgi | grep -v grep | grep 9010 | awk '{ print $2 }' | xargs kill
echo Stopped...
echo Wait...
sleep 1
uwsgi --socket :9010 --wsgi-file Actarium/wsgi.py -d logfile.log
echo Started...




