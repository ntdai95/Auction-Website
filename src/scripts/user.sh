#!/bin/bash
cd ../users
export FLASK_APP=user.py
flask run --port=5001 &