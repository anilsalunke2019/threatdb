#!/bin/bash
git clone https://github.com/appyens/threat-intelligent-hub /var/www/html/threat-intelligent-hub/
pip install -r /requirements.txt
python3 /var/www/html/threat-intelligent-hub/manage.py
