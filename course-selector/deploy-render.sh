#!/bin/bash

# Deploy script for Render.com
# Usage: ./deploy-render.sh

echo "Deploying to Render.com..."

# Check if render CLI is installed
if ! command -v render &> /dev/null; then
    echo "Installing Render CLI..."
    npm install -g @render/cli
fi

# Deploy
render deploy

echo "Deploy script complete. Check your Render dashboard for status."