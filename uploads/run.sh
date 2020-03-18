#!/bin/bash
cd /var/www/html/; git clone https://github.com/appyens/threat-intelligent-hub.git .;find  -type d -exec chmod 755 {} + ;find -type f -exec chmod 644 {} +;chown -R www-data:www-data *;
sed -i -r 's/172.16.0.207$/0.0.0.0/g' /var/www/html/manage.py
sed -i -r 's/8888$/80/g'
exec python3 -m pip install -r /requirements.txt
python3 /var/www/html/manage.py

exit 0
