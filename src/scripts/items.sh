#!/bin/bash
cd ../items/core
export FLASK_APP=restful_items.py
flask run --port=5003 &