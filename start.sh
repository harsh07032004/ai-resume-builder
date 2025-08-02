#!/bin/bash

echo "🚀 Starting AI Resume Generator..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is not installed"
    exit 1
fi

if ! command_exists pdflatex; then
    echo "❌ LaTeX (pdflatex) is not installed"
    echo "   Please run: sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended"
    exit 1
fi

echo "✅ All prerequisites are installed"

# Start backend
echo "🔧 Starting backend server..."
cd backend

if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "📦 Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install -q -r requirements.txt

echo "🌐 Starting Flask server on http://localhost:5000..."
python app.py &
BACKEND_PID=$!

cd ..

# Start frontend
echo "🎨 Starting frontend server..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

echo "🌐 Starting React development server on http://localhost:3000..."
npm start &
FRONTEND_PID=$!

cd ..

# Wait a moment for servers to start
sleep 3

echo ""
echo "🎉 AI Resume Generator is now running!"
echo ""
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend:  http://localhost:5000"
echo "📍 Health:   http://localhost:5000/health"
echo ""
echo "💡 Tips:"
echo "   • Fill out the form with your resume information"
echo "   • Toggle 'Enhance with AI' for improved descriptions"
echo "   • Click 'Preview Resume' to see the result"
echo "   • Click 'Download PDF' to get your professional resume"
echo ""
echo "🛑 To stop the servers, press Ctrl+C"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait