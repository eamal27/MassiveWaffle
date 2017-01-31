#!/bin/bash

gunicorn --chdir /MassiveWaffle --bind 0.0.0.0:8000 server:app

