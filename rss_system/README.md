# RSS Feed System for Marc Pinet's Website

A robust RSS feed generation system that monitors new content across multiple sections of the website and generates feeds only for new entries (not modifications).

## Features

- **Multi-section monitoring**: Tracks posts, projects, work experiences, education, and certifications
- **Smart detection**: Only notifies for genuinely new entries, not modifications
- **Multiple feeds**: Generates individual feeds per section plus a master feed
- **State persistence**: Maintains history to avoid duplicate notifications
- **Robust parsing**: Handles various content formats and structures

## Setup

### Prerequisites
- Python 3.6+
- pip

### Installation

**Windows:**
```cmd
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Manual:**
```bash
pip install -r requirements.txt
```

## Usage

### Basic Commands

```bash
# Generate RSS feeds (only new entries)
python main.py

# Check current status without generating
python main.py --status

# Force regenerate all feeds (treat all as new)
python main.py --force

# Enable verbose output
python main.py --verbose
```

### Automated Execution

**Windows (Task Scheduler):**
```cmd
run_rss_generator.bat
```

**Linux/Mac (Cron):**
```bash
chmod +x run_rss_generator.sh
# Add to crontab for regular execution
# Example: Run every hour
# 0 * * * * /path/to/run_rss_generator.sh
```

## Generated Feeds

The system generates the following RSS feeds in `static/feeds/`:

- `posts.xml` - Blog posts and articles
- `projects.xml` - New projects
- `experiences.xml` - Work experience updates
- `education.xml` - Educational achievements
- `certifications.xml` - New certifications
- `all.xml` - Master feed with all content types
- `../atom.xml` - Alias for the master feed

## Feed URLs

- Posts: `https://marcpinet.fr/feeds/posts.xml`
- Projects: `https://marcpinet.fr/feeds/projects.xml`
- Experiences: `https://marcpinet.fr/feeds/experiences.xml`
- Education: `https://marcpinet.fr/feeds/education.xml`
- Certifications: `https://marcpinet.fr/feeds/certifications.xml`
- All (Master): `https://marcpinet.fr/feeds/all.xml`
- All (Atom): `https://marcpinet.fr/atom.xml`

## How It Works

### Content Detection

1. **Posts & Projects**: Parsed from individual markdown files in `/content/posts/` and `/content/projects/`
2. **Experiences, Education, Certifications**: Extracted from structured sections in `/content/about.md`

### Uniqueness Detection

Each entry gets a unique ID based on:
- Content type
- Key identifying information (title, company, dates, etc.)
- Metadata hash

### State Management

The system maintains a `rss_state.json` file that tracks:
- Previously seen entry IDs
- Last generation timestamp
- Known entries per content type

### New Entry Criteria

An entry is considered "new" if:
- Its unique ID hasn't been seen before
- It passes the content validation checks

## Configuration

Modify `config.py` to customize:
- Base URL
- Feed descriptions
- Maximum entries per feed
- Output directories

## File Structure

```
rss_system/
├── main.py              # Main CLI interface
├── rss_generator.py     # Core RSS generation logic
├── content_parser.py    # Content parsing from various sources
├── state_manager.py     # State persistence and tracking
├── feed_templates.py    # RSS XML generation
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── setup.sh/.bat       # Setup scripts
├── run_rss_generator.sh/.bat  # Automated execution scripts
└── README.md           # This file
```

## Troubleshooting

### Common Issues

**"No new entries found"**
- Normal if no content has been added since last run
- Use `--force` to regenerate all feeds
- Check `--status` to see current state

**"Content directory not found"**
- Ensure the script is run from the correct directory
- Verify the website structure matches expected paths

**"Permission denied"**
- Ensure write permissions to `static/` directory
- On Unix systems, make scripts executable: `chmod +x *.sh`

### Logs

Automated runs log to `rss_generator.log` in the same directory.

## Integration with GitHub Actions

To automatically generate RSS feeds on content updates, add this to `.github/workflows/rss.yml`:

```yaml
name: Generate RSS Feeds

on:
  push:
    paths:
      - 'content/**'
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  generate-rss:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          cd rss_system
          pip install -r requirements.txt
      - name: Generate RSS feeds
        run: |
          cd rss_system
          python main.py
      - name: Commit and push feeds
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add static/feeds/ static/atom.xml static/rss_state.json
          git commit -m "Update RSS feeds" || exit 0
          git push
```

## License

This RSS system is part of Marc Pinet's personal website project.
