#!/usr/bin/env python3

import os
import re

def add_rss_links_to_site():
    """Add RSS feed links to the website's base template"""
    
    base_template_path = os.path.join('..', 'templates', 'base.html')
    
    if not os.path.exists(base_template_path):
        print(f"❌ Base template not found at {base_template_path}")
        return False
    
    with open(base_template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    rss_links = '''    <!-- RSS Feeds -->
    <link rel="alternate" type="application/rss+xml" title="Marc Pinet - All Updates" href="/atom.xml" />
    <link rel="alternate" type="application/rss+xml" title="Marc Pinet - Blog Posts" href="/feeds/posts.xml" />
    <link rel="alternate" type="application/rss+xml" title="Marc Pinet - Projects" href="/feeds/projects.xml" />
    <link rel="alternate" type="application/rss+xml" title="Marc Pinet - Work Experience" href="/feeds/experiences.xml" />
    <link rel="alternate" type="application/rss+xml" title="Marc Pinet - Education" href="/feeds/education.xml" />
    <link rel="alternate" type="application/rss+xml" title="Marc Pinet - Certifications" href="/feeds/certifications.xml" />'''
    
    if 'RSS Feeds' in content:
        print("⚠️  RSS links already present in base template")
        return True
    
    head_pattern = r'(<head[^>]*>)'
    match = re.search(head_pattern, content)
    
    if not match:
        print("❌ Could not find <head> tag in base template")
        return False
    
    updated_content = content.replace(
        match.group(1),
        match.group(1) + '\n' + rss_links
    )
    
    with open(base_template_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("✅ RSS feed links added to base template")
    return True

def create_rss_subscription_page():
    """Create a page where users can subscribe to RSS feeds"""
    
    rss_page_content = """+++
title = "RSS Feeds"
path = "rss"
+++

# 📡 RSS Feeds

Stay updated with the latest content from my website by subscribing to these RSS feeds:

## 🎯 Master Feed (All Content)
Subscribe to get notified about all new posts, projects, experiences, education updates, and certifications.

**Feed URL:** [`/atom.xml`](/atom.xml)

## 📝 Specific Feeds

Choose the specific types of content you're interested in:

### 📰 Blog Posts & Articles
Get notified when I publish new blog posts and articles.

**Feed URL:** [`/feeds/posts.xml`](/feeds/posts.xml)

### 🚀 Projects
Stay updated with my latest projects and developments.

**Feed URL:** [`/feeds/projects.xml`](/feeds/projects.xml)

### 💼 Work Experience
Get notified about my career updates and new professional experiences.

**Feed URL:** [`/feeds/experiences.xml`](/feeds/experiences.xml)

### 🎓 Education
Stay informed about my educational achievements and academic updates.

**Feed URL:** [`/feeds/education.xml`](/feeds/education.xml)

### 🪪 Certifications
Get notified when I earn new certifications and professional achievements.

**Feed URL:** [`/feeds/certifications.xml`](/feeds/certifications.xml)

## 🔧 How to Use RSS Feeds

RSS feeds allow you to stay updated without manually checking the website. You can use:

- **Feed readers**: [Feedly](https://feedly.com/), [Inoreader](https://www.inoreader.com/), [NewsBlur](https://newsblur.com/)
- **Email notifications**: Services like [Blogtrottr](https://blogtrottr.com/) 
- **Browser extensions**: Many browsers support RSS feed subscriptions
- **Mobile apps**: Most RSS readers have mobile apps

Simply copy the feed URL and add it to your preferred RSS reader.

---

*Note: These feeds only notify about genuinely new content, not modifications to existing entries.*"""

    rss_page_path = os.path.join('..', 'content', 'rss.md')
    
    with open(rss_page_path, 'w', encoding='utf-8') as f:
        f.write(rss_page_content)
    
    print("✅ RSS subscription page created at /content/rss.md")
    return True

def update_menu_with_rss():
    """Add RSS to the website menu"""
    
    config_path = os.path.join('..', 'config.toml')
    
    if not os.path.exists(config_path):
        print(f"❌ Config file not found at {config_path}")
        return False
    
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'name = "RSS"' in content:
        print("⚠️  RSS already in menu")
        return True
    
    menu_pattern = r'(menu = \[.*?)\]'
    match = re.search(menu_pattern, content, re.DOTALL)
    
    if not match:
        print("❌ Could not find menu section in config")
        return False
    
    rss_menu_item = '    { name = "RSS", url = "/rss", weight = 3, icon = "rss.png" },'
    
    updated_menu = match.group(1) + '\n' + rss_menu_item + '\n]'
    updated_content = content.replace(match.group(0), updated_menu)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("✅ RSS menu item added to config.toml")
    print("⚠️  Note: You'll need to add an rss.png icon to static/menu_icon/")
    return True

def main():
    print("🔧 Adding RSS Integration to Website")
    print("=" * 50)
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    success = True
    
    success &= add_rss_links_to_site()
    success &= create_rss_subscription_page()
    success &= update_menu_with_rss()
    
    if success:
        print("\n✅ RSS integration completed successfully!")
        print("\n📋 Next steps:")
        print("1. Add an RSS icon (rss.png) to static/menu_icon/")
        print("2. Generate the RSS feeds: python main.py")
        print("3. Build and deploy your website")
    else:
        print("\n❌ Some steps failed. Check the messages above.")

if __name__ == "__main__":
    main()
