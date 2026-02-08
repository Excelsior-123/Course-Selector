#!/bin/bash

# Deploy script for Railway
# Usage: ./deploy-railway.sh

echo "Deploying to Railway..."

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login and deploy
railway login
railway link
railway up

echo "Deploy script complete. Check your Railway dashboard for status."