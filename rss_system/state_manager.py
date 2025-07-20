import json
import os
from typing import Dict, List, Set
from datetime import datetime

class StateManager:
    def __init__(self, state_file: str = 'rss_state.json'):
        self.state_file = state_file
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        return {
            'last_check': None,
            'known_entries': {
                'posts': set(),
                'projects': set(),
                'experiences': set(),
                'education': set(),
                'certifications': set()
            }
        }
    
    def save_state(self):
        state_to_save = {
            'last_check': datetime.now().isoformat(),
            'known_entries': {
                key: list(value) if isinstance(value, set) else value
                for key, value in self.state['known_entries'].items()
            }
        }
        
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state_to_save, f, indent=2, ensure_ascii=False)
    
    def _ensure_sets(self):
        for key in self.state['known_entries']:
            if isinstance(self.state['known_entries'][key], list):
                self.state['known_entries'][key] = set(self.state['known_entries'][key])
    
    def get_new_entries(self, content_type: str, entries: List[Dict]) -> List[Dict]:
        self._ensure_sets()
        
        if content_type not in self.state['known_entries']:
            self.state['known_entries'][content_type] = set()
        
        known_ids = self.state['known_entries'][content_type]
        new_entries = []
        
        for entry in entries:
            entry_id = entry.get('id')
            if entry_id and entry_id not in known_ids:
                new_entries.append(entry)
        
        return new_entries
    
    def mark_entries_as_seen(self, content_type: str, entries: List[Dict]):
        self._ensure_sets()
        
        if content_type not in self.state['known_entries']:
            self.state['known_entries'][content_type] = set()
        
        for entry in entries:
            entry_id = entry.get('id')
            if entry_id:
                self.state['known_entries'][content_type].add(entry_id)
    
    def is_first_run(self) -> bool:
        return self.state.get('last_check') is None
    
    def get_last_check(self) -> str:
        return self.state.get('last_check', '')
    
    def reset_state(self):
        self.state = {
            'last_check': None,
            'known_entries': {
                'posts': set(),
                'projects': set(),
                'experiences': set(),
                'education': set(),
                'certifications': set()
            }
        }
        self.save_state()
