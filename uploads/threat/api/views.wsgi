#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
"""
A wsgi script for hosting flask app with apache
Created on 21/10/2019
@author: Anurag
"""

# imports
import sys
import logging

activate_this = '/home/threat-intelligent-hub/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
sys.path.insert(0, "/home/threat-intelligent-hub")
logging.basicConfig(stream=sys.stderr)


