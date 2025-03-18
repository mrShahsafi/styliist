#!/bin/bash

# Activate the virtual environment
source venv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }

# Install dependencies
pip install -r requirements.txt || { echo "Failed to install dependencies"; exit 1; }

# Load environment variables from env_variables.txt if the file exists
if [ -f env_variables.txt ]; then
    export $(grep -v '^#' env_variables.txt | xargs)
fi

# Apply migrations
python manage.py migrate || { echo "Migrations failed"; exit 1; }

# Start Redis server in daemon mode
redis-server --daemonize yes || { echo "Failed to start Redis"; exit 1; }
sleep 2

# Run tests
python manage.py test || { echo "Tests failed"; exit 1; }

# Seed the database
python manage.py seed_all || { echo "Seeding failed"; exit 1; }

# Start Django Q in the background
python manage.py qcluster &

# Start Django development server
python manage.py runserver