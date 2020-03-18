#!/bin/bash
exec cd /var/www/html/; git clone https://github.com/appyens/threat-intelligent-hub.git .;find  -type d -exec chmod 755 {} + ;find -type f -exec chmod 644 {} +;chown -R www-data:www-data *;
exec python3 -m pip install -r /requirements.txt;
exec python3 /var/www/html/manage.py;

exit 0
