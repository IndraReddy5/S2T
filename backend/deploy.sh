#!/bin/bash

# Check if .env file exists
if [ ! -f .env ]; then
  echo "Error: .env file not found. Please create the .env file before running this script."
  exit 1
fi

# Stop running containers
echo "Stopping running containers ..."
docker compose down

# Delete old images
echo "Delete old docker image ..."
docker image rm backend-api:latest

# Checkout the `main` branch
git checkout main

# Pull the changes from main
git pull

# Deploy the current version
echo "Building and deploying containers ..."
docker compose up -d 
