@echo off
echo 🔧 Setting up RSS Feed System for Marc Pinet's Website
echo ======================================================

cd /d "%~dp0"

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not found
    pause
    exit /b 1
)

echo 📦 Installing Python dependencies...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo ✅ Dependencies installed successfully
) else (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo 🎯 RSS System Setup Complete!
echo.
echo Usage:
echo   python main.py              # Generate RSS feeds
echo   python main.py --status     # Check current status
echo   python main.py --force      # Force regenerate all feeds
echo   python main.py --verbose    # Enable verbose output
echo.
echo 📂 Feeds will be generated in: ../static/feeds/
echo 🌐 Master feed will be available at: /atom.xml
echo.
pause
