#!/bin/bash
exec git clone https://github.com/appyens/threat-intelligent-hub /var/www/html/
exec pip install -r /requirements.txt
exec python3 /var/www/html/manage.py
