#!/bin/bash
uwsgi --socket :9000 --wsgi-file Actarium/wsgi.py -d logfile.log


