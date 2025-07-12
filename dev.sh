#!/bin/bash

# HelloSonar AI Development Script

echo "🚀 Starting HelloSonar AI in development mode..."

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

# Function to cleanup background processes
cleanup() {
    echo "🛑 Stopping development servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Start backend
echo "🔧 Starting backend server..."
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "🔧 Starting frontend server..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo "✅ Development servers started!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
echo "📊 Health check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for background processes
wait 