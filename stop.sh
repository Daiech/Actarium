#!/bin/bash
ps -Af | grep uwsgi | grep -v grep | grep 9010 | awk '{ print $2 }' | xargs kill



