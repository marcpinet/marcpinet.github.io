#!/usr/bin/env python3
import argparse
import sys
from config import Config
from rss_manager import RSSManager

def main():
    parser = argparse.ArgumentParser(description='RSS Feed Generator for Marc Pinet\'s Website')
    parser.add_argument('--force', action='store_true',
                       help='Force regenerate all feeds (treat all entries as new)')
    parser.add_argument('--status', action='store_true',
                       help='Show current status without generating feeds')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--clean', action='store_true',
                       help='Clean cache and regenerate all feeds')
   
    args = parser.parse_args()
   
    try:
        Config.validate_paths()
       
        manager = RSSManager(
            content_root=Config.CONTENT_ROOT,
            output_dir=Config.OUTPUT_ROOT,
            base_url=Config.BASE_URL,
            site_title=getattr(Config, 'SITE_TITLE', 'Marc Pinet')
        )
       
        if args.clean:
            manager.clear_cache()
            if args.verbose:
                print("Cache cleared")
        
        if args.status:
            show_status(manager, args.verbose)
            return
       
        if args.verbose:
            print(f"Content root: {Config.CONTENT_ROOT}")
            print(f"Output directory: {Config.OUTPUT_ROOT}")
            print(f"Base URL: {Config.BASE_URL}")
            print("-" * 50)
       
        print("Generating RSS feeds...")
       
        if args.force:
            manager.clear_cache()
            
        feed_stats = manager.generate_all_feeds()
       
        print("\nRSS Feed Generation Complete!")
        print("=" * 50)
       
        display_results(feed_stats, args.verbose)
       
        print(f"\nFeeds generated in: {Config.get_feeds_directory()}")
        print("Available feeds:")
        for feed_type in Config.FEED_TYPES.keys():
            print(f"  - {Config.BASE_URL}/feeds/{feed_type}.xml")
        print(f"  - {Config.BASE_URL}/feeds/all.xml (master feed)")
        print(f"  - {Config.BASE_URL}/atom.xml (master feed alias)")
       
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

def show_status(manager: RSSManager, verbose: bool = False):
    print("RSS System Status")
    print("=" * 50)
   
    status = manager.get_status()
   
    if status['is_first_run']:
        print("First run detected - no previous state found")
    else:
        print(f"Last update: {status['last_update']}")
   
    print("\nContent Summary:")
    total_content = sum(status['content_counts'].values())
    for content_type, count in status['content_counts'].items():
        print(f"  - {content_type.title()}: {count} entries")
    print(f"  Total: {total_content} entries")
   
    print("\nNew Entries (since last run):")
    total_new = sum(status['new_entries_counts'].values())
    if total_new > 0:
        for content_type, count in status['new_entries_counts'].items():
            if count > 0:
                print(f"  - {content_type.title()}: {count} new entries")
        print(f"  Total new: {total_new}")
    else:
        print("  No new entries detected")
   
    print("\nFeed Files Status:")
    feeds_dir = manager.feeds_dir  # Changement ici
    feed_files = {
        'posts': feeds_dir / 'posts.xml',
        'projects': feeds_dir / 'projects.xml', 
        'experiences': feeds_dir / 'experiences.xml',
        'education': feeds_dir / 'education.xml',
        'certifications': feeds_dir / 'certifications.xml',
        'all': feeds_dir / 'all.xml'
    }
    
    for feed_name, feed_path in feed_files.items():
        exists = feed_path.exists()
        status_icon = "[EXISTS]" if exists else "[MISSING]"
        size_info = ""
        if exists and verbose:
            size = feed_path.stat().st_size
            modified = feed_path.stat().st_mtime
            from datetime import datetime
            mod_time = datetime.fromtimestamp(modified).strftime('%Y-%m-%d %H:%M')
            size_info = f" ({size:,} bytes, modified: {mod_time})"
        print(f"  {status_icon} {feed_name}.xml{size_info}")
   
    if not any(feed_path.exists() for feed_path in feed_files.values()):
        print("\nRun without --status to generate feeds")
    
    if verbose:
        print(f"\nCache file: {manager.cache_file}")
        print(f"Cache exists: {manager.cache_file.exists()}")

def display_results(feed_stats: dict, verbose: bool = False):
    total_entries = sum(count for count in feed_stats.values() if isinstance(count, int))
    new_entries = feed_stats.get('new_entries', {})
    total_new = sum(new_entries.values()) if new_entries else 0
    
    if verbose:
        print("Detailed Statistics:")
        print("-" * 30)
        for feed_type, count in feed_stats.items():
            if feed_type != 'new_entries' and isinstance(count, int):
                new_count = new_entries.get(feed_type, 0) if new_entries else 0
                new_indicator = f" ({new_count} new)" if new_count > 0 else ""
                print(f"  {feed_type.title()}: {count} total entries{new_indicator}")
        print(f"  Total: {total_entries} entries")
        
        if total_new > 0:
            print(f"\nNew entries added to feeds: {total_new}")
        else:
            print("\nNo new entries added (all content already in feeds)")
    else:
        if total_new > 0:
            print(f"Summary: {total_new} new entries added across all feeds")
            for feed_type, count in new_entries.items():
                if count > 0:
                    print(f"  - {feed_type.title()}: {count} new entries")
        else:
            print("No new entries found - all feeds are up to date")

if __name__ == "__main__":
    main()