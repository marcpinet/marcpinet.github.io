# 🤖 Automatic README Fetcher

This system automatically fetches README.md content from your GitHub repositories and includes it in your project pages with full GitHub markdown support.

## How it works

1. **Script Analysis**: The `fetch_readmes.py` script reads all project files in `content/projects/`
2. **GitHub Integration**: For each project with a `link_to` pointing to a GitHub repo, it fetches the README.md
3. **GitHub Markdown Processing**: Converts GitHub-specific markdown features to HTML
4. **Content Injection**: The processed README content is automatically added to your project page
5. **Auto-Update**: GitHub Actions runs this daily and on every push

## 🎯 GitHub Markdown Features Supported

### 📸 **Images & Media**
- ✅ **Relative Images**: `![alt](path/image.jpg)` → `![alt](https://raw.githubusercontent.com/user/repo/main/path/image.jpg)`
- ✅ **Relative Videos**: `![alt](video.mp4)` → HTML `<video>` tags with controls
- ✅ **HTML img tags**: Automatic URL conversion for relative paths

### 🎨 **GitHub Alerts**
```markdown
> [!NOTE]
> This is a note

> [!TIP]
> This is a tip

> [!IMPORTANT]
> This is important

> [!WARNING]
> This is a warning

> [!CAUTION]
> This is caution
```
All converted to styled HTML divs with proper colors and icons.

### ✅ **Task Lists**
```markdown
- [ ] Unchecked task
- [x] Checked task
- [ ] Another task
```
Converted to HTML checkboxes (disabled for display).

### 📊 **Enhanced Tables**
GitHub-style tables with improved responsive styling and wrapper divs.

## Setup

### Automatic (GitHub Actions)
✅ Already configured! The system will:
- Run automatically on every push to main branch
- Run daily at 2 AM UTC to fetch updated READMEs
- Process all GitHub markdown features
- Commit any changes back to your repository

### Manual Testing (Local)

#### Windows:
```bash
cd scripts
test_local.bat
```

#### Linux/Mac:
```bash
cd scripts
chmod +x test_local.sh
./test_local.sh
```

## Project File Format

Your project markdown files should have this structure:

```toml
+++
title = "Project Name"
description = "Short description..."
date = "2024-01-01"
weight = 1

[extra]
remote_image = "/project/img.gif"
link_to = "https://github.com/yourusername/yourrepo"  # 👈 This triggers README fetching
pinned = true
pin_order = 1
+++

# This content will be replaced with the processed GitHub README.md
```

## 🔧 Processing Features

### **Image Conversion**
```markdown
# Before (in your GitHub README)
![Demo](resources/demo.gif)

# After (in your website)
![Demo](https://raw.githubusercontent.com/user/repo/main/resources/demo.gif)
```

### **Video Conversion**
```markdown
# Before (in your GitHub README)
![Demo Video](demo.mp4)

# After (in your website)
<video controls style="max-width: 100%; height: auto;">
    <source src="https://raw.githubusercontent.com/user/repo/main/demo.mp4" type="video/mp4">
    Your browser does not support the video tag.
</video>
```

### **Alert Conversion**
```markdown
# Before (in your GitHub README)
> [!WARNING]
> Be careful with this feature!

# After (in your website)
<div class="github-alert github-alert-warning">
    ⚠️ WARNING: Be careful with this feature!
</div>
```

## Features

- ✅ **Automatic fetching** from GitHub repositories
- ✅ **Smart title handling** (removes duplicate titles)
- ✅ **Fallback branches** (tries main, then master)
- ✅ **Error handling** (continues if a README can't be fetched)
- ✅ **Daily updates** via GitHub Actions
- ✅ **Local testing** support
- ✅ **Full GitHub markdown support** (alerts, tasks, images, videos)
- ✅ **Responsive styling** for all elements
- ✅ **SEO-friendly** HTML output

## Files Created

- `scripts/fetch_readmes.py` - Main fetching script with GitHub markdown processing
- `scripts/requirements.txt` - Python dependencies
- `scripts/test_local.sh` - Local testing script (Linux/Mac)
- `scripts/test_local.bat` - Local testing script (Windows)
- `.github/workflows/build.yml` - Updated to include README fetching

## Supported Video Formats

- ✅ MP4 (`.mp4`)
- ✅ WebM (`.webm`)
- ✅ OGG (`.ogg`)
- ✅ MOV (`.mov`)
- ✅ AVI (`.avi`)
- ✅ MKV (`.mkv`)
- ✅ M4V (`.m4v`)

## CSS Classes Added

The script automatically adds CSS for:
- `.github-alert` and variants for each alert type
- `.table-wrapper` for responsive tables
- Checkbox styling for task lists
- Video responsive styling

## How to Add New Projects

1. Create a new `.md` file in `content/projects/`
2. Add the frontmatter with `link_to` pointing to your GitHub repo
3. Push to main branch
4. The README will be automatically fetched and all GitHub features converted!

## Troubleshooting

### README not fetching?
- Check that `link_to` points to a valid GitHub repository
- Ensure the repository has a README.md file
- Check the GitHub Actions log for error messages

### Images not showing?
- Ensure your images use relative paths in the GitHub README
- The script automatically converts `![alt](path/img.jpg)` to absolute URLs

### Videos not working?
- Make sure videos are in supported formats
- Use markdown image syntax: `![alt](video.mp4)`
- Videos will be converted to HTML5 `<video>` tags automatically

### Alerts not styling correctly?
- Use exact GitHub alert syntax: `> [!NOTE]`
- Supported types: NOTE, TIP, IMPORTANT, WARNING, CAUTION
- CSS is automatically injected

### Want to exclude a project?
- Simply don't include `link_to` in the frontmatter
- Or point `link_to` to something other than GitHub

### Need to update immediately?
- Run the local test script
- Or manually trigger the GitHub Action from the Actions tab