@echo off
setlocal

set RSS_DIR=%~dp0
set LOG_FILE=%RSS_DIR%rss_generator.log

echo %date% %time%: Starting RSS feed generation >> "%LOG_FILE%"

cd /d "%RSS_DIR%"

python main.py >> "%LOG_FILE%" 2>&1

if %errorlevel% equ 0 (
    echo %date% %time%: RSS feed generation completed successfully >> "%LOG_FILE%"
) else (
    echo %date% %time%: RSS feed generation failed >> "%LOG_FILE%"
    exit /b 1
)
