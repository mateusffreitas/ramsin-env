#!/bin/bash
set -e
python3 -m venv venv
source venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt 
python3 -m nuitka --onefile --standalone --static-libpython=no ramsin_env.py
deactivate
