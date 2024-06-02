#!/bin/bash

echo "Starting the server..."
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
