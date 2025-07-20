from datetime import datetime
from typing import List, Dict
import xml.etree.ElementTree as ET
from xml.dom import minidom
import html

class FeedTemplates:
    def __init__(self, base_url: str = "https://marcpinet.fr", title: str = "Marc Pinet"):
        self.base_url = base_url.rstrip('/')
        self.title = title
    
    def generate_rss_feed(self, entries: List[Dict], feed_type: str, description: str) -> str:
        rss = ET.Element("rss", version="2.0")
        rss.set("xmlns:atom", "http://www.w3.org/2005/Atom")
        
        channel = ET.SubElement(rss, "channel")
        
        ET.SubElement(channel, "title").text = f"{self.title} - {feed_type.title()}"
        ET.SubElement(channel, "link").text = f"{self.base_url}"
        ET.SubElement(channel, "description").text = description
        ET.SubElement(channel, "language").text = "en-us"
        ET.SubElement(channel, "lastBuildDate").text = self._format_rfc822_date(datetime.now())
        ET.SubElement(channel, "generator").text = "Custom RSS Generator"
        
        atom_link = ET.SubElement(channel, "atom:link")
        atom_link.set("href", f"{self.base_url}/feeds/{feed_type}.xml")
        atom_link.set("rel", "self")
        atom_link.set("type", "application/rss+xml")
        
        for entry in entries:
            item = self._create_item(entry, feed_type)
            channel.append(item)
        
        return self._prettify_xml(rss)
    
    def _create_item(self, entry: Dict, feed_type: str) -> ET.Element:
        item = ET.Element("item")
        
        title = self._get_entry_title(entry, feed_type)
        ET.SubElement(item, "title").text = title
        
        link = self._get_entry_link(entry, feed_type)
        ET.SubElement(item, "link").text = link
        
        description = self._get_entry_description(entry, feed_type)
        ET.SubElement(item, "description").text = description
        
        pub_date = self._get_entry_date(entry)
        if pub_date:
            ET.SubElement(item, "pubDate").text = self._format_rfc822_date(pub_date)
        
        guid = ET.SubElement(item, "guid")
        entry_type = entry.get('type', feed_type)
        
        if entry_type in ['post', 'project']:
            guid.text = link
            guid.set("isPermaLink", "true")
        else:
            guid.text = f"marcpinet.fr:{entry_type}:{entry.get('id', '')}"
            guid.set("isPermaLink", "false")
        
        if entry.get('fields'):
            for field in entry['fields'][:5]:
                if field.strip():
                    ET.SubElement(item, "category").text = field.strip()
        
        return item
    
    def _get_entry_title(self, entry: Dict, feed_type: str) -> str:
        entry_type = entry.get('type', feed_type)
        
        if entry_type == 'post':
            return entry.get('title', 'New Post')
        elif entry_type == 'project':
            title = entry.get('title', 'New Project')
            return f"New Project: {title}"
        elif entry_type == 'experience':
            position = entry.get('position', '')
            company = entry.get('company', '')
            if position and company:
                return f"New Position: {position} at {company}"
            return "New Work Experience"
        elif entry_type == 'education':
            degree = entry.get('degree', '')
            institution = entry.get('institution', '')
            if degree and institution:
                return f"New Education: {degree} at {institution}"
            return "New Educational Achievement"
        elif entry_type == 'certification':
            title = entry.get('title', '')
            return f"New Certification: {title}" if title else "New Certification"
        else:
            return entry.get('title', 'New Entry')
    
    def _get_entry_link(self, entry: Dict, feed_type: str) -> str:
        entry_type = entry.get('type', feed_type)
        
        if entry_type == 'post':
            filename = entry.get('filename', '')
            slug = filename.replace('.md', '') if filename else 'unknown'
            return f"{self.base_url}/posts/{slug}/"
        elif entry_type == 'project':
            filename = entry.get('filename', '')
            slug = filename.replace('.md', '') if filename else 'unknown'
            return f"{self.base_url}/projects/{slug}/"
        elif entry_type in ['experience', 'education', 'certification']:
            # Pointer vers la page about avec une ancre si possible
            return f"{self.base_url}/about/"
        else:
            return self.base_url
    
    def _get_entry_description(self, entry: Dict, feed_type: str) -> str:
        entry_type = entry.get('type', feed_type)
        
        if entry_type == 'post':
            description = entry.get('description', '')
            if not description:
                description = "New blog post published"
            return description
        
        elif entry_type == 'project':
            description = entry.get('description', '')
            if not description:
                description = "New project added to portfolio"
            
            # Add technologies if available
            fields = entry.get('fields', [])
            if fields:
                tech_list = ', '.join(fields[:5])  # Limit to 5 technologies
                description += f" | Technologies: {tech_list}"
            
            return description
        
        elif entry_type == 'experience':
            parts = []
            
            if entry.get('position'):
                parts.append(f"Position: {entry['position']}")
            if entry.get('company'):
                parts.append(f"Company: {entry['company']}")
            if entry.get('period'):
                parts.append(f"Duration: {entry['period']}")
            
            description = entry.get('description', '')
            if description:
                parts.append(f"Summary: {description}")
            
            # Add key technologies/skills
            fields = entry.get('fields', [])
            if fields:
                key_skills = ', '.join(fields[:4])  # Limit to 4 key skills
                parts.append(f"Key Technologies: {key_skills}")
            
            return ' | '.join(parts)
        
        elif entry_type == 'education':
            parts = []
            
            if entry.get('degree'):
                parts.append(f"Degree: {entry['degree']}")
            if entry.get('institution'):
                parts.append(f"Institution: {entry['institution']}")
            if entry.get('period'):
                parts.append(f"Period: {entry['period']}")
            
            description = entry.get('description', '')
            if description:
                parts.append(f"Details: {description}")
            
            # Add focus areas
            fields = entry.get('fields', [])
            if fields:
                focus_areas = ', '.join(fields[:4])  # Limit to 4 focus areas
                parts.append(f"Focus Areas: {focus_areas}")
            
            return ' | '.join(parts)
        
        elif entry_type == 'certification':
            parts = []
            
            if entry.get('title'):
                parts.append(f"Certification: {entry['title']}")
            if entry.get('issued'):
                parts.append(f"Issued: {entry['issued']}")
            
            # Add relevant areas
            fields = entry.get('fields', [])
            if fields:
                areas = ', '.join(fields)
                parts.append(f"Areas: {areas}")
            
            return ' | '.join(parts)
        
        return 'New entry added'
    
    def _get_entry_date(self, entry: Dict) -> datetime:
        date_str = entry.get('date', '')
        if not date_str:
            return datetime.now()
        
        try:
            if 'T' in date_str:
                return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                return datetime.strptime(date_str, '%Y-%m-%d')
        except:
            return datetime.now()
    
    def _format_rfc822_date(self, dt: datetime) -> str:
        return dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    def _prettify_xml(self, elem: ET.Element) -> str:
        rough_string = ET.tostring(elem, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        pretty = reparsed.toprettyxml(indent="  ", encoding=None)
        
        # Remove empty lines and clean up
        lines = [line for line in pretty.split('\n') if line.strip()]
        return '\n'.join(lines[1:])  # Remove the XML declaration line
    
    def generate_master_feed(self, all_new_entries: Dict[str, List[Dict]]) -> str:
        all_entries = []
        for feed_type, entries in all_new_entries.items():
            all_entries.extend(entries)
        
        # Sort by date, most recent first
        all_entries.sort(key=lambda x: self._get_entry_date(x), reverse=True)
        
        return self.generate_rss_feed(
            all_entries[:50], 
            "all", 
            "All updates from Marc Pinet - new posts, projects, work experiences, education, and certifications"
        )