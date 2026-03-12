#!/bin/bash

# Task Automation Suite - Web Server Startup Script

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   Task Automation Suite - Web UI                          ║"
echo "║   One-Click Task Creation Interface                       ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo ""
    echo "Please create .env file with your credentials:"
    echo ""
    echo "  cp .env.example .env"
    echo "  nano .env"
    echo ""
    exit 1
fi

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt -q

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies"
    exit 1
fi

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
python3 -m playwright install chromium -q

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   ✅ Setup Complete!                                      ║"
echo "║                                                           ║"
echo "║   🚀 Starting Web Server...                              ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "📍 Open your browser:"
echo ""
echo "   👉 http://localhost:5000"
echo ""
echo "✨ Ready to create tasks!"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the web server
python3 web_server.py
