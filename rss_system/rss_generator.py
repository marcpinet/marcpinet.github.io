from datetime import datetime
from typing import List, Dict, Optional
import xml.etree.ElementTree as ET
from xml.dom import minidom
from dataclasses import asdict

class RSSFeedGenerator:
    def __init__(self, base_url: str = "https://marcpinet.fr", site_title: str = "Marc Pinet"):
        self.base_url = base_url.rstrip('/')
        self.site_title = site_title
        
        self.feed_configs = {
            'posts': {
                'title': 'Posts',
                'description': 'Latest blog posts and articles',
                'url_template': '/posts/{slug}/'
            },
            'projects': {
                'title': 'Projects', 
                'description': 'New projects and developments',
                'url_template': '/projects/{slug}/'
            },
            'experiences': {
                'title': 'Experiences',
                'description': 'Latest work experiences and career updates',
                'url_template': '/about/'
            },
            'education': {
                'title': 'Education',
                'description': 'Educational achievements and academic updates',
                'url_template': '/about/'
            },
            'certifications': {
                'title': 'Certifications',
                'description': 'New certifications and professional achievements',
                'url_template': '/about/'
            }
        }
    
    def generate_feed(self, entries: List, feed_type: str) -> str:
        config = self.feed_configs.get(feed_type, {
            'title': feed_type.title(),
            'description': f'Updates from {self.site_title}',
            'url_template': '/'
        })
        
        rss = self._create_rss_root()
        channel = self._create_channel(config, feed_type)
        rss.append(channel)
        
        for entry in entries[:50]:
            item = self._create_item(entry, feed_type, config)
            channel.append(item)
        
        return self._format_xml(rss)
    
    def generate_master_feed(self, all_entries: Dict[str, List]) -> str:
        combined_entries = []
        for feed_type, entries in all_entries.items():
            combined_entries.extend(entries)
        
        combined_entries.sort(key=lambda x: self._parse_date(x.date), reverse=True)
        
        config = {
            'title': 'All Updates',
            'description': 'All updates from Marc Pinet - posts, projects, experiences, education, and certifications',
            'url_template': '/'
        }
        
        rss = self._create_rss_root()
        channel = self._create_channel(config, 'all')
        rss.append(channel)
        
        for entry in combined_entries[:50]:
            item = self._create_item(entry, entry.type, self.feed_configs.get(entry.type, config))
            channel.append(item)
        
        return self._format_xml(rss)
    
    def _create_rss_root(self) -> ET.Element:
        rss = ET.Element("rss", version="2.0")
        rss.set("xmlns:atom", "http://www.w3.org/2005/Atom")
        return rss
    
    def _create_channel(self, config: Dict, feed_type: str) -> ET.Element:
        channel = ET.Element("channel")
        
        ET.SubElement(channel, "title").text = f"{self.site_title} - {config['title']}"
        ET.SubElement(channel, "link").text = self.base_url
        ET.SubElement(channel, "description").text = config['description']
        ET.SubElement(channel, "language").text = "en-us"
        ET.SubElement(channel, "lastBuildDate").text = self._format_rfc822(datetime.now())
        ET.SubElement(channel, "generator").text = "Custom RSS Generator"
        
        atom_link = ET.SubElement(channel, "atom:link")
        atom_link.set("href", f"{self.base_url}/feeds/{feed_type}.xml")
        atom_link.set("rel", "self")
        atom_link.set("type", "application/rss+xml")
        
        return channel
    
    def _create_item(self, entry, feed_type: str, config: Dict) -> ET.Element:
        item = ET.Element("item")
        
        title = self._get_item_title(entry, feed_type)
        ET.SubElement(item, "title").text = title
        
        link = self._get_item_link(entry, feed_type, config)
        ET.SubElement(item, "link").text = link
        
        description = self._get_item_description(entry, feed_type)
        ET.SubElement(item, "description").text = description
        
        pub_date = self._parse_date(entry.date)
        ET.SubElement(item, "pubDate").text = self._format_rfc822(pub_date)
        
        guid = ET.SubElement(item, "guid")
        if entry.type in ['post', 'project']:
            guid.text = link
            guid.set("isPermaLink", "true")
        else:
            guid.text = f"marcpinet.fr:{entry.type}:{entry.id}"
            guid.set("isPermaLink", "false")
        
        for field in entry.fields[:5]:
            if field.strip():
                ET.SubElement(item, "category").text = field.strip()
        
        return item
    
    def _get_item_title(self, entry, feed_type: str) -> str:
        title_generators = {
            'post': lambda e: e.title,
            'project': lambda e: f"New Project: {e.title}",
            'experience': lambda e: f"New Position: {e.metadata.get('position', '')} at {e.metadata.get('company', '')}",
            'education': lambda e: f"New Education: {e.metadata.get('degree', '')} at {e.metadata.get('institution', '')}",
            'certification': lambda e: f"New Certification: {e.metadata.get('title', '')}"
        }
        
        generator = title_generators.get(entry.type, lambda e: e.title)
        return generator(entry) or "New Entry"
    
    def _get_item_link(self, entry, feed_type: str, config: Dict) -> str:
        if entry.type in ['post', 'project']:
            slug = entry.filename.replace('.md', '') if entry.filename else 'unknown'
            return f"{self.base_url}{config['url_template'].format(slug=slug)}"
        else:
            return f"{self.base_url}{config['url_template']}"
    
    def _get_item_description(self, entry, feed_type: str) -> str:
        if entry.type in ['post', 'project']:
            description = entry.description or f"New {entry.type} published"
            if entry.fields and entry.type == 'project':
                tech_list = ', '.join(entry.fields[:5])
                description += f" | Technologies: {tech_list}"
            return description
        
        elif entry.type == 'experience':
            parts = []
            metadata = entry.metadata
            
            if metadata.get('position'):
                parts.append(f"Position: {metadata['position']}")
            if metadata.get('company'):
                parts.append(f"Company: {metadata['company']}")
            if metadata.get('period'):
                parts.append(f"Duration: {metadata['period']}")
            
            if entry.description:
                parts.append(f"Summary: {entry.description}")
            
            if entry.fields:
                key_skills = ', '.join(entry.fields[:4])
                parts.append(f"Key Technologies: {key_skills}")
            
            return ' | '.join(parts)
        
        elif entry.type == 'education':
            parts = []
            metadata = entry.metadata
            
            if metadata.get('degree'):
                parts.append(f"Degree: {metadata['degree']}")
            if metadata.get('institution'):
                parts.append(f"Institution: {metadata['institution']}")
            if metadata.get('period'):
                parts.append(f"Period: {metadata['period']}")
            
            if entry.description:
                parts.append(f"Details: {entry.description}")
            
            if entry.fields:
                focus_areas = ', '.join(entry.fields[:4])
                parts.append(f"Focus Areas: {focus_areas}")
            
            return ' | '.join(parts)
        
        elif entry.type == 'certification':
            parts = []
            metadata = entry.metadata
            
            if metadata.get('title'):
                parts.append(f"Certification: {metadata['title']}")
            if metadata.get('issued'):
                parts.append(f"Issued: {metadata['issued']}")
            
            if entry.fields:
                areas = ', '.join(entry.fields)
                parts.append(f"Areas: {areas}")
            
            return ' | '.join(parts)
        
        return entry.description or 'New entry added'
    
    def _parse_date(self, date_str: str) -> datetime:
        if not date_str:
            return datetime.now()
        
        try:
            if 'T' in date_str:
                return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                return datetime.strptime(date_str, '%Y-%m-%d')
        except (ValueError, TypeError):
            return datetime.now()
    
    def _format_rfc822(self, dt: datetime) -> str:
        return dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    def _format_xml(self, elem: ET.Element) -> str:
        rough_string = ET.tostring(elem, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        pretty = reparsed.toprettyxml(indent="  ", encoding=None)
        
        lines = [line for line in pretty.split('\n') if line.strip()]
        return '\n'.join(lines[1:])