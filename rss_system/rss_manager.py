import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from content_parser import ContentParser
from rss_generator import RSSFeedGenerator

class RSSManager:
    def __init__(self, content_root: str, output_dir: str, base_url: str = "https://marcpinet.fr", site_title: str = "Marc Pinet"):
        self.parser = ContentParser(content_root)
        self.generator = RSSFeedGenerator(base_url, site_title)
        self.output_dir = Path(output_dir)
        self.feeds_dir = self.output_dir / 'feeds'
        self.feeds_dir.mkdir(parents=True, exist_ok=True)
        
        self.cache_file = self.feeds_dir / 'rss_cache.json'
        self.previous_content = self._load_cache()
    
    def generate_all_feeds(self) -> Dict[str, int]:
        current_content = self.parser.parse_all_content()
        new_entries = self._find_new_entries(current_content)
        
        stats = {}
        feed_types = ['posts', 'projects', 'experiences', 'education', 'certifications']
        
        for feed_type in feed_types:
            entries = current_content.get(feed_type, [])
            if entries:
                feed_xml = self.generator.generate_feed(entries, feed_type)
                self._write_feed(f"{feed_type}.xml", feed_xml)
                stats[feed_type] = len(entries)
            else:
                stats[feed_type] = 0
        
        master_feed = self.generator.generate_master_feed(current_content)
        self._write_feed("all.xml", master_feed)
        self._write_feed("atom.xml", master_feed)
        
        stats['new_entries'] = {
            feed_type: len(entries) for feed_type, entries in new_entries.items()
        }
        
        self._save_cache(current_content)
        self.copy_master_feed_to_root()
        
        return stats
    
    def get_status(self) -> Dict:
        current_content = self.parser.parse_all_content()
        new_entries = self._find_new_entries(current_content)
        
        is_first_run = not self.cache_file.exists() or not self.previous_content
        last_update = None
        
        if self.cache_file.exists():
            try:
                mod_time = self.cache_file.stat().st_mtime
                last_update = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
            except OSError:
                pass
        
        return {
            'is_first_run': is_first_run,
            'last_update': last_update,
            'content_counts': {
                feed_type: len(entries) for feed_type, entries in current_content.items()
            },
            'new_entries_counts': {
                feed_type: len(entries) for feed_type, entries in new_entries.items()
            }
        }
    
    def clear_cache(self) -> None:
        if self.cache_file.exists():
            self.cache_file.unlink()
        self.previous_content = {}
    
    def _find_new_entries(self, current_content: Dict[str, List]) -> Dict[str, List]:
        if not self.previous_content:
            return current_content
        
        new_entries = {}
        
        for feed_type, entries in current_content.items():
            previous_ids = {item['id'] for item in self.previous_content.get(feed_type, [])}
            current_new = [entry for entry in entries if entry.id not in previous_ids]
            new_entries[feed_type] = current_new
        
        return new_entries
    
    def _load_cache(self) -> Dict:
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('content', {})
            except (json.JSONDecodeError, FileNotFoundError, KeyError):
                pass
        return {}
    
    def _save_cache(self, content: Dict[str, List]) -> None:
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'content': {}
        }
        
        for feed_type, entries in content.items():
            cache_data['content'][feed_type] = [
                {
                    'id': entry.id, 
                    'date': entry.date,
                    'title': entry.title
                } for entry in entries
            ]
        
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)
    
    def _write_feed(self, filename: str, content: str) -> None:
        feed_path = self.feeds_dir / filename
        with open(feed_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
            
    def copy_master_feed_to_root(self) -> None:
        source = self.feeds_dir / 'atom.xml'
        destination = self.output_dir / 'atom.xml'
        
        if source.exists():
            import shutil
            try:
                shutil.copy2(source, destination)
                print(f"✅ Copied master feed to root: {destination}")
                
                if destination.exists():
                    size = destination.stat().st_size
                    print(f"✅ Root atom.xml created successfully ({size} bytes)")
                else:
                    print("❌ Failed to create root atom.xml")
            except Exception as e:
                print(f"❌ Error copying atom.xml: {e}")
        else:
            print(f"❌ Source file not found: {source}")
            # Lister ce qui existe dans feeds/
            if self.feeds_dir.exists():
                files = list(self.feeds_dir.glob("*.xml"))
                print(f"Available XML files: {[f.name for f in files]}")