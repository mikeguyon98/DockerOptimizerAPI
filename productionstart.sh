#!/bin/sh

# Start the Docker daemon in the background
dockerd &

# Wait for the Docker daemon to start
until docker info; do
    echo "Waiting for the Docker daemon to start..."
    sleep 1
done

# Now run the main application
exec gunicorn -w 2 -b 0.0.0.0:5000 "app:app"