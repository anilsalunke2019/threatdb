#!/usr/bin/env bash

ENV_ROOT="$PWD/venv"

if [ ! -d $ENV_ROOT ]; then
  pip3 || pip3.6 install virtualenv
  python3 || python3.6 -m virtualenv venv
  source ./venv/bin/activate
  pip3 || pip3.6 install -r requirements.txt
  python3 || python3.6 main.py
else
  source ./venv/bin/activate
  python3 || python3.6 main.py
fi
