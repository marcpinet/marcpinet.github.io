#!/bin/bash

echo "🔄 Testing README fetching system..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if we're in the right directory
if [ ! -d "content/projects" ]; then
    echo "❌ Please run this script from the root of your marcpinet.github.io repository"
    exit 1
fi

echo "📦 Installing Python dependencies..."
cd scripts
pip install -r requirements.txt

echo "🔍 Fetching README content..."
python fetch_readmes.py

echo "✅ Done! Check your content/projects/ files to see the updates."
echo "💡 Tip: Run 'zola serve' to test your site locally."