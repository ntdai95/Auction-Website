#!/bin/bash
cd ../auctions
export FLASK_APP=restful_auctions.py
flask run --port=5002 &