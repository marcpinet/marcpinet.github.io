#!/bin/bash

RSS_DIR="$(dirname "$0")"
LOG_FILE="$RSS_DIR/rss_generator.log"

echo "$(date): Starting RSS feed generation" >> "$LOG_FILE"

cd "$RSS_DIR"

python3 main.py >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "$(date): RSS feed generation completed successfully" >> "$LOG_FILE"
else
    echo "$(date): RSS feed generation failed" >> "$LOG_FILE"
    exit 1
fi
