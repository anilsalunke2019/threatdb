#!/bin/bash
find /var/www/html/threat/ -type d -exec chmod 755 {} + ;find /var/www/html/threat/ -type f -exec chmod 644 {} +;chown -R www-data:www-data *;exec /usr/bin/python3 -m pip install -r /requirements.txt;exec /usr/bin/python3 /var/www/html/threat/manage.py;
exec supervisord -n
