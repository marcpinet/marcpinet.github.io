#!/bin/bash

echo "🔧 Setting up RSS Feed System for Marc Pinet's Website"
echo "======================================================"

cd "$(dirname "$0")"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    exit 1
fi

echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "🎯 RSS System Setup Complete!"
echo ""
echo "Usage:"
echo "  python3 main.py              # Generate RSS feeds"
echo "  python3 main.py --status     # Check current status"
echo "  python3 main.py --force      # Force regenerate all feeds"
echo "  python3 main.py --verbose    # Enable verbose output"
echo ""
echo "📂 Feeds will be generated in: ../static/feeds/"
echo "🌐 Master feed will be available at: /atom.xml"
