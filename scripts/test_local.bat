@echo off
echo 🔄 Testing README fetching system...

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed.
    exit /b 1
)

REM Check if we're in the right directory
if not exist "content\projects" (
    echo ❌ Please run this script from the root of your marcpinet.github.io repository
    exit /b 1
)

echo 📦 Installing Python dependencies...
cd scripts
pip install -r requirements.txt

echo 🔍 Fetching README content...
python fetch_readmes.py

echo ✅ Done! Check your content/projects/ files to see the updates.
echo 💡 Tip: Run 'zola serve' to test your site locally.