import os
import sys

def validate_system():
    try:
        print("🔍 Validating RSS System Setup")
    except UnicodeEncodeError:
        print("Validating RSS System Setup")
    
    success = True
    
    required_files = [
        'main.py',
        'rss_generator.py', 
        'content_parser.py',
        'state_manager.py',
        'feed_templates.py',
        'config.py'
    ]
    
    try:
        print("✅ Checking required files...")
    except UnicodeEncodeError:
        print("Checking required files...")
    
    for file in required_files:
        if not os.path.exists(file):
            try:
                print(f"❌ Missing: {file}")
            except UnicodeEncodeError:
                print(f"Missing: {file}")
            success = False
        else:
            try:
                print(f"✅ Found: {file}")
            except UnicodeEncodeError:
                print(f"Found: {file}")
    
    try:
        print("📁 Checking directory structure...")
    except UnicodeEncodeError:
        print("Checking directory structure...")
    
    content_dir = os.path.join('..', 'content')
    static_dir = os.path.join('..', 'static')
    
    if not os.path.exists(content_dir):
        try:
            print(f"❌ Content directory not found: {content_dir}")
        except UnicodeEncodeError:
            print(f"Content directory not found: {content_dir}")
        success = False
    else:
        try:
            print(f"✅ Content directory found: {content_dir}")
        except UnicodeEncodeError:
            print(f"Content directory found: {content_dir}")
    
    if not os.path.exists(static_dir):
        try:
            print(f"❌ Static directory not found: {static_dir}")
        except UnicodeEncodeError:
            print(f"Static directory not found: {static_dir}")
        success = False
    else:
        try:
            print(f"✅ Static directory found: {static_dir}")
        except UnicodeEncodeError:
            print(f"Static directory found: {static_dir}")
    
    try:
        print("🐍 Checking Python version...")
    except UnicodeEncodeError:
        print("Checking Python version...")
    
    if sys.version_info < (3, 6):
        try:
            print("❌ Python 3.6+ required")
        except UnicodeEncodeError:
            print("Python 3.6+ required")
        success = False
    else:
        try:
            print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
        except UnicodeEncodeError:
            print(f"Python {sys.version_info.major}.{sys.version_info.minor}")
    
    try:
        import feedgen
        print("✅ feedgen module available")
    except ImportError:
        try:
            print("❌ feedgen module not found")
        except UnicodeEncodeError:
            print("feedgen module not found")
        success = False
    except UnicodeEncodeError:
        print("feedgen module available")
    
    if success:
        try:
            print("🎉 System validation passed!")
        except UnicodeEncodeError:
            print("System validation passed!")
    else:
        try:
            print("❌ System validation failed")
        except UnicodeEncodeError:
            print("System validation failed")
    
    return success

if __name__ == "__main__":
    success = validate_system()
    sys.exit(0 if success else 1)