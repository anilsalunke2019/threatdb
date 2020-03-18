#!/bin/bash
cd /var/www/html/;
exec /usr/bin/git clone https://github.com/appyens/threat-intelligent-hub.git /var/www/html/;find  /var/www/html/ -type d -exec chmod 755 {} + ;find /var/www/html/ -type f -exec chmod 644 {} +;chown -R www-data:www-data *;
exec /usr/bin/python3 -m pip install -r /requirements.txt;
exec /usr/bin/python3 /var/www/html/manage.py;

exit 0
