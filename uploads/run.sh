#!/bin/bash
exec /usr/bin/python3 -m pip install -r /requirements.txt;exec /usr/bin/python3 /var/www/html/threat/manage.py;
exec supervisord -n
