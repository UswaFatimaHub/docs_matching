#!/bin/bash

# Start APScheduler in the background
echo "🕒 Starting APScheduler..."
python manage.py runapscheduler &

# Start Gunicorn in the foreground
echo "🚀 Starting Gunicorn..."
exec gunicorn embedding_project.wsgi:application --bind 0.0.0.0:8000 --timeout 300 --preload