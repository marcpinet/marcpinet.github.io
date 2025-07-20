#!/usr/bin/env python3

import os
import sys

def validate_system():
    print("🔍 Validating RSS System Setup")
    print("=" * 50)
    
    print("📂 Checking directory structure...")
    required_dirs = [
        '../content',
        '../content/posts',
        '../content/projects',
        '../static',
        '../static/feeds'
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ❌ {dir_path} - Missing")
            return False
    
    print("\n📄 Checking required files...")
    required_files = [
        '../content/about.md',
        '../config.toml',
        'main.py',
        'rss_generator.py',
        'content_parser.py',
        'state_manager.py',
        'feed_templates.py',
        'config.py'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - Missing")
            return False
    
    print("\n📊 Checking content availability...")
    
    projects_dir = '../content/projects'
    project_files = [f for f in os.listdir(projects_dir) if f.endswith('.md') and not f.startswith('_')]
    print(f"  📁 Projects: {len(project_files)} found")
    
    with open('../content/about.md', 'r', encoding='utf-8') as f:
        about_content = f.read()
    
    sections = {
        'experiences': '💼 Work Experience' in about_content,
        'education': '🎓 Education' in about_content,
        'certifications': '🪪 Certifications' in about_content
    }
    
    for section, found in sections.items():
        status = "✅" if found else "❌"
        print(f"  {status} {section.title()} section in about.md")
    
    print("\n✅ System validation completed successfully!")
    return True

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    success = validate_system()
    if success:
        print("\n🚀 Ready to generate RSS feeds!")
        print("   Run: python main.py --status")
    sys.exit(0 if success else 1)
