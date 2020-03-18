#!/bin/bash
exec /usr/bin/python3 -m pip install -r /requirements.txt;
exec supervisord -n
