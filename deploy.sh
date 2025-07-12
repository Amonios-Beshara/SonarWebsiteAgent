#!/bin/bash

# HelloSonar AI Deployment Script

set -e

echo "🚀 Starting HelloSonar AI deployment..."

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "❌ Error: backend/.env file not found!"
    echo "Please create backend/.env with the following variables:"
    echo "LIVEKIT_API_KEY=your_livekit_api_key"
    echo "LIVEKIT_API_SECRET=your_livekit_api_secret"
    echo "LIVEKIT_URL=wss://your-livekit-server.com"
    echo "OPENAI_API_KEY=your_openai_api_key"
    exit 1
fi

# Build and deploy backend
echo "🔧 Building backend..."
cd backend
docker build -t hellosonar-backend .
cd ..

# Build and deploy frontend
echo "🔧 Building frontend..."
cd frontend
docker build -t hellosonar-frontend .
cd ..

# Run with docker-compose
echo "🚀 Starting services with docker-compose..."
docker-compose up -d

echo "✅ Deployment complete!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
echo "📊 Health check: http://localhost:8000/health"

# Show running containers
echo "📋 Running containers:"
docker-compose ps 