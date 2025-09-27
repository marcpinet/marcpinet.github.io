#!/usr/bin/env python3
import os
import requests
import re
from pathlib import Path

def extract_github_repo(link_to):
    """Extract owner/repo from GitHub URL"""
    match = re.search(r'github\.com/([^/]+)/([^/]+)', link_to)
    if match:
        return match.group(1), match.group(2)
    return None, None

def fetch_readme(owner, repo):
    """Fetch README.md content from GitHub"""
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        pass
    
    # Try master branch if main doesn't exist
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/README.md"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        pass
    
    return None

def convert_relative_images(content, owner, repo, branch="main"):
    """Convert relative image paths to absolute GitHub URLs"""
    base_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/"
    
    # Pattern for markdown images: ![alt](path)
    def replace_image(match):
        alt_text = match.group(1)
        image_path = match.group(2)
        
        # Skip if already absolute URL
        if image_path.startswith(('http://', 'https://', '//')):
            return match.group(0)
        
        # Convert relative path to absolute GitHub URL
        absolute_url = base_url + image_path
        return f"![{alt_text}]({absolute_url})"
    
    # Replace markdown images
    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_image, content)
    
    # Also handle HTML img tags
    def replace_html_img(match):
        src = match.group(1)
        rest = match.group(2)
        
        if src.startswith(('http://', 'https://', '//')):
            return match.group(0)
        
        absolute_url = base_url + src
        return f'<img src="{absolute_url}"{rest}>'
    
    content = re.sub(r'<img\s+src="([^"]+)"([^>]*)>', replace_html_img, content)
    
    return content

def convert_github_video_urls(content, owner, repo):
    """Convert standalone GitHub user-attachments video URLs to HTML video tags"""
    
    # Pattern to match GitHub user-attachments URLs on their own line
    pattern = r'^https://github\.com/user-attachments/assets/[a-f0-9-]+$'
    
    def replace_video_url(match):
        video_url = match.group(0)
        return f'''<video controls style="max-width: 100%; height: auto;">
    <source src="{video_url}" type="video/mp4">
    Your browser does not support the video tag. <a href="{video_url}">View video</a>
</video>'''
    
    # Replace standalone GitHub video URLs
    content = re.sub(pattern, replace_video_url, content, flags=re.MULTILINE)
    
    return content

def convert_relative_videos(content, owner, repo, branch="main"):
    """Convert relative video paths and GitHub user-attachments to HTML video tags"""
    base_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/"
    
    # Video extensions
    video_extensions = r'\.(mp4|webm|ogg|mov|avi|mkv|m4v)$'
    
    def replace_video_link(match):
        alt_text = match.group(1) or "Video"
        video_path = match.group(2)
        
        # Skip if already absolute URL (except GitHub user-attachments)
        if video_path.startswith(('http://', 'https://', '//')):
            # Check if it's a GitHub user-attachments video
            if 'github.com/user-attachments/assets/' in video_path:
                # Convert GitHub user-attachments to video tag
                return f'''<video controls style="max-width: 100%; height: auto;">
    <source src="{video_path}" type="video/mp4">
    Your browser does not support the video tag. <a href="{video_path}">View video</a>
</video>'''
            else:
                return match.group(0)
        
        # Skip if not a video file
        if not re.search(video_extensions, video_path, re.IGNORECASE):
            return match.group(0)
        
        absolute_url = base_url + video_path
        
        # Convert to HTML video tag
        return f'''<video controls style="max-width: 100%; height: auto;">
    <source src="{absolute_url}" type="video/{video_path.split('.')[-1]}">
    Your browser does not support the video tag. <a href="{absolute_url}">Download video</a>
</video>'''
    
    # Replace markdown-style video links ![alt](video.mp4)
    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_video_link, content)
    
    return content

def convert_github_alerts(content):
    """Convert GitHub-style alerts to HTML"""
    
    # GitHub alert patterns
    alert_patterns = {
        'NOTE': ('note', '💡', '#0969da'),
        'TIP': ('tip', '💡', '#1a7f37'),
        'IMPORTANT': ('important', '❗', '#8250df'),
        'WARNING': ('warning', '⚠️', '#d1242f'),
        'CAUTION': ('caution', '🚨', '#d1242f')
    }
    
    for alert_type, (css_class, icon, color) in alert_patterns.items():
        # Pattern: > [!NOTE] or > [!NOTE]\n> content
        pattern = rf'> \[!{alert_type}\]\s*\n((?:> .*\n?)*)'
        
        def replace_alert(match):
            alert_content = match.group(1)
            # Remove the '> ' prefix from each line
            clean_content = re.sub(r'^> ', '', alert_content, flags=re.MULTILINE)
            clean_content = clean_content.strip()
            
            return f'''<div class="github-alert github-alert-{css_class}" style="border-left: 4px solid {color}; background-color: {color}10; padding: 12px 16px; margin: 16px 0; border-radius: 6px;">
    <div style="display: flex; align-items: flex-start;">
        <span style="margin-right: 8px; font-size: 16px;">{icon}</span>
        <div style="flex: 1;">
            <strong style="color: {color}; text-transform: uppercase; font-size: 14px; font-weight: 600;">{alert_type}</strong>
            <div style="margin-top: 4px;">{clean_content}</div>
        </div>
    </div>
</div>'''
        
        content = re.sub(pattern, replace_alert, content, flags=re.MULTILINE)
    
    return content

def convert_task_lists(content):
    """Convert GitHub-style task lists to normal bullet points"""
    
    # Convert unchecked tasks to normal bullet points
    content = re.sub(
        r'^(\s*)[-*]\s+\[\s\]\s+(.*)$',
        r'\1- \2',
        content,
        flags=re.MULTILINE
    )
    
    # Convert checked tasks to normal bullet points with "✓" prefix
    content = re.sub(
        r'^(\s*)[-*]\s+\[[xX]\]\s+(.*)$',
        r'\1- ✓ \2',
        content,
        flags=re.MULTILINE
    )
    
    return content

import re
import markdown

def convert_github_tables(content):
    """Convert markdown tables to HTML tables with wrapper"""
    lines = content.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if '|' in line and i + 1 < len(lines) and re.match(r'^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$', lines[i + 1]):
            header = [c.strip() for c in line.strip().strip('|').split('|')]
            i += 2
            rows = []
            while i < len(lines) and '|' in lines[i]:
                row = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                rows.append(row)
                i += 1

            table_html = '<div class="table-wrapper">\n<table>\n<thead>\n<tr>'
            for h in header:
                table_html += f'<th>{markdown.markdown(h)}</th>'
            table_html += '</tr>\n</thead>\n<tbody>\n'

            for row in rows:
                table_html += '<tr>'
                for c in row:
                    table_html += f'<td>{markdown.markdown(c)}</td>'
                table_html += '</tr>\n'

            table_html += '</tbody>\n</table>\n</div>'
            result.append(table_html)
        else:
            result.append(line)
            i += 1

    return '\n'.join(result)

def convert_relative_links(content, owner, repo, branch="main"):
    """Convert relative links to absolute GitHub URLs"""
    base_url = f"https://github.com/{owner}/{repo}/tree/{branch}/"
    
    # Pattern for markdown links: [text](path)
    def replace_link(match):
        link_text = match.group(1)
        link_path = match.group(2)
        
        # Skip if already absolute URL, anchor link, or special protocols
        if link_path.startswith(('http://', 'https://', '//', '#', 'mailto:', 'tel:', 'ftp:')):
            return match.group(0)
        
        # Skip if it's an image (already handled by convert_relative_images)
        if link_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp')):
            return match.group(0)
        
        # Convert relative path to absolute GitHub URL
        absolute_url = base_url + link_path
        return f"[{link_text}]({absolute_url})"
    
    # Replace markdown links
    content = re.sub(r'\[([^\]]*)\]\(([^)]+)\)', replace_link, content)
    
    return content

def fix_code_blocks_and_spacing(content):
    """Fix code blocks and ensure proper spacing around all elements"""
    import re

    def space_html(s):
        s = re.sub(r'([^\n])(<div)', r'\1\n\n\2', s)
        s = re.sub(r'(</div>)([^\n])', r'\1\n\n\2', s)
        s = re.sub(r'([^\n])(<video)', r'\1\n\n\2', s)
        s = re.sub(r'(</video>)([^\n])', r'\1\n\n\2', s)
        
        # FIX: Ensure headings have 2 newlines before them
        s = re.sub(r'([^#\n])(\n?)(#{1,6}\s+.*)', r'\1\n\n\3', s)
        
        # FIX: Ensure images have 2 newlines before them
        s = re.sub(r'([^\n\[])(\n?)(\!\[[^\]]*\]\([^)]+\))', r'\1\n\n\3', s)
        
        return s

    content = re.sub(r'```[ \t]*\n+([A-Za-z0-9_#+-]+)\n', r'```\1\n', content)

    parts = []
    last = 0
    pattern = re.compile(r'```([^\n]*)\n(.*?)\n```', re.DOTALL)

    for m in pattern.finditer(content):
        before = content[last:m.start()]
        before = space_html(before)
        before = re.sub(r' +\n', '\n', before)
        if before and not before.endswith('\n\n'):
            before = re.sub(r'\n*$', '', before) + '\n\n'

        lang = m.group(1)
        code = re.sub(r'\n+$', '', m.group(2))
        block = f'```{lang}\n{code}\n```' if lang else f'```\n{code}\n```'
        parts.append(before + block)
        last = m.end()

    tail = content[last:]
    tail = space_html(tail)
    tail = re.sub(r' +\n', '\n', tail)

    result = ''.join(parts) + tail
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result

def add_github_styles(content):
    """Add CSS styles for GitHub-specific elements"""
    
    styles = '''
<style>
/* GitHub Alert Styles */
.github-alert {
    border-radius: 6px;
    margin: 16px 0;
    padding: 12px 16px;
    border-left: 4px solid;
}

.github-alert-note {
    background-color: #ddf4ff;
    border-color: #0969da;
}

.github-alert-tip {
    background-color: #dcfce7;
    border-color: #1a7f37;
}

.github-alert-important {
    background-color: #f3e8ff;
    border-color: #8250df;
}

.github-alert-warning {
    background-color: #fff8dc;
    border-color: #d1242f;
}

.github-alert-caution {
    background-color: #ffebee;
    border-color: #d1242f;
}

/* Table Wrapper */
.table-wrapper {
    overflow-x: auto;
    margin: 16px 0;
}

.table-wrapper table {
    width: 100%;
    border-collapse: collapse;
}

.table-wrapper th,
.table-wrapper td {
    border: 1px solid #d1d5da;
    padding: 8px 12px;
    text-align: left;
}

.table-wrapper th {
    font-weight: 600;
}

/* Video Styles */
video {
    max-width: 100%;
    height: auto;
    border-radius: 6px;
    margin: 16px 0;
}

/* Code Block Styles */
pre {
    background-color: #f6f8fa;
    border-radius: 6px;
    padding: 16px;
    overflow-x: auto;
    margin: 16px 0;
}

code {
    background-color: #f6f8fa;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: 'SFMono-Regular', 'Monaco', 'Inconsolata', 'Liberation Mono', 'Consolas', monospace;
    font-size: 85%;
    color: #24292f;
}

pre code {
    background-color: transparent;
    padding: 0;
}

/* Dark mode support for inline code */
@media (prefers-color-scheme: dark) {
    pre {
        background-color: #161b22;
        color: #f0f6fc;
    }
    
    code {
        background-color: #21262d;
        color: #f0f6fc;
    }
    
    pre code {
        background-color: transparent;
        color: inherit;
    }
}
</style>

'''
    
    return styles + content

def process_readme_content(content, owner, repo):
    """Process README content with all GitHub-specific conversions"""
    if not content:
        return content
    
    print(f"  🔄 Processing README content...")
    
    # 1. Convert relative images to absolute URLs
    content = convert_relative_images(content, owner, repo)
    print(f"  ✅ Converted relative images")
    
    # 2. Convert relative links to absolute URLs
    content = convert_relative_links(content, owner, repo)
    print(f"  ✅ Converted relative links")
    
    # 3. Convert relative videos to HTML video tags
    content = convert_relative_videos(content, owner, repo)
    print(f"  ✅ Converted relative videos")

    # 3.5. Convert standalone GitHub video URLs
    content = convert_github_video_urls(content, owner, repo)
    print(f"  ✅ Converted GitHub video URLs")
    
    # 4. Convert GitHub alerts
    content = convert_github_alerts(content)
    print(f"  ✅ Converted GitHub alerts")
    
    # 5. Convert task lists to normal bullet points
    content = convert_task_lists(content)
    print(f"  ✅ Converted task lists")
    
    # 6. Improve table rendering
    content = convert_github_tables(content)
    print(f"  ✅ Enhanced tables")
    
    # 7. Fix code blocks and spacing (AFTER all HTML generation)
    content = fix_code_blocks_and_spacing(content)
    print(f"  ✅ Fixed code blocks and spacing")
    
    # 8. Add GitHub-specific styles
    content = add_github_styles(content)
    print(f"  ✅ Added GitHub styles")
    
    return content

def process_project_file(file_path):
    """Process a single project markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract frontmatter
    if not content.startswith('+++'):
        return
    
    parts = content.split('+++', 2)
    if len(parts) < 3:
        return
    
    frontmatter = parts[1]
    existing_body = parts[2].strip()
    
    # Extract link_to from frontmatter
    link_match = re.search(r'link_to\s*=\s*"([^"]+)"', frontmatter)
    if not link_match:
        return
    
    link_to = link_match.group(1)
    owner, repo = extract_github_repo(link_to)
    
    if not owner or not repo:
        return
    
    print(f"Processing {file_path.name}: {owner}/{repo}")
    
    # Fetch README content
    readme_content = fetch_readme(owner, repo)
    if not readme_content:
        print(f"  ⚠️  Could not fetch README for {owner}/{repo}")
        return
    
    # Process README content with GitHub-specific conversions
    readme_content = process_readme_content(readme_content, owner, repo)
    
    # Clean up README content
    # Remove title if it matches the project title
    title_match = re.search(r'title\s*=\s*"([^"]+)"', frontmatter)
    if title_match:
        title = title_match.group(1)
        # Remove first h1 if it matches title
        readme_content = re.sub(rf'^#\s+{re.escape(title)}\s*\n', '', readme_content, flags=re.MULTILINE)
    
    # Build new content
    new_content = f"+++{frontmatter}+++"
    
    if readme_content.strip():
        new_content += f"\n\n{readme_content.strip()}"
    elif existing_body:
        new_content += f"\n\n{existing_body}"
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✅ Updated {file_path.name}")

def main():
    """Main function to process all project files"""
    projects_dir = Path("../content/projects")
    
    if not projects_dir.exists():
        print("❌ Projects directory not found!")
        return
    
    print("🔄 Fetching README content for all projects...")
    
    for md_file in projects_dir.glob("*.md"):
        if md_file.name == "_index.md":
            continue
        
        try:
            process_project_file(md_file)
        except Exception as e:
            print(f"  ❌ Error processing {md_file.name}: {e}")
    
    print("✅ Done!")

if __name__ == "__main__":
    main()