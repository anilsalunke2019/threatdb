#!/bin/bash
cd /var/www/html/; git clone https://github.com/appyens/threat-intelligent-hub.git .;find  -type d -exec chmod 755 {} + ;find -type f -exec chmod 644 {} +;chown -R www-data:www-data *;
exec pip3 install -r /requirements.txt -n
