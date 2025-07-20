import os
import re
import hashlib
import json
import toml
from datetime import datetime
from typing import Dict, List, Optional, Union, Tuple
from pathlib import Path
import frontmatter
import html
from dataclasses import dataclass, asdict

@dataclass
class ContentItem:
    id: str
    type: str
    title: str
    description: str
    date: str
    content: str = ""
    filename: str = ""
    metadata: Dict = None
    fields: List[str] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.fields is None:
            self.fields = []

class ContentParser:
    def __init__(self, content_root: str):
        self.content_root = Path(content_root)
        self.date_patterns = [
            (r'\d{4}-\d{2}-\d{2}', '%Y-%m-%d'),
            (r'\w{3} \d{4}', '%b %Y'),
            (r'\d{4}', '%Y'),
        ]
        
    def parse_all_content(self) -> Dict[str, List[ContentItem]]:
        return {
            'posts': self.parse_posts(),
            'projects': self.parse_projects(),
            'experiences': self.parse_experiences(),
            'education': self.parse_education(),
            'certifications': self.parse_certifications()
        }
    
    def parse_posts(self) -> List[ContentItem]:
        return self._parse_markdown_directory('posts', 'post')
    
    def parse_projects(self) -> List[ContentItem]:
        return self._parse_markdown_directory('projects', 'project')
    
    def _parse_markdown_directory(self, directory: str, content_type: str) -> List[ContentItem]:
        items = []
        dir_path = self.content_root / directory
        
        if not dir_path.exists():
            return items
            
        for file_path in dir_path.glob('*.md'):
            if not file_path.name.startswith('_'):
                item = self._parse_markdown_file(file_path, content_type)
                if item:
                    items.append(item)
                    
        return sorted(items, key=lambda x: x.date, reverse=True)
    
    def _parse_markdown_file(self, filepath: Path, content_type: str) -> Optional[ContentItem]:
        try:
            raw_content = filepath.read_text(encoding='utf-8')
            
            if raw_content.strip().startswith('+++'):
                metadata, content = self._parse_toml_frontmatter(raw_content)
            else:
                with open(filepath, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                metadata = post.metadata
                content = post.content
            
            title = self._clean_text(metadata.get('title', filepath.stem))
            description = metadata.get('description', '')
            
            if not description and content:
                description = self._extract_description(content, 400)
            
            date_str = self._normalize_date(str(metadata.get('date', '')))
            unique_id = self._generate_id(content_type, filepath.name, metadata)
            
            return ContentItem(
                id=unique_id,
                type=content_type,
                title=title,
                description=description,
                date=date_str,
                content=content,
                filename=filepath.name,
                metadata=metadata
            )
        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
            return None
    
    def _parse_toml_frontmatter(self, content: str) -> Tuple[Dict, str]:
        lines = content.strip().split('\n')
        
        if lines[0] != '+++':
            return {}, content
        
        frontmatter_lines = []
        content_start = 0
        
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == '+++':
                content_start = i + 1
                break
            frontmatter_lines.append(line)
        
        if content_start == 0:
            return {}, content
        
        try:
            toml_str = '\n'.join(frontmatter_lines)
            metadata = toml.loads(toml_str)
            markdown_content = '\n'.join(lines[content_start:]).strip()
            return metadata, markdown_content
        except Exception as e:
            print(f"Error parsing TOML frontmatter: {e}")
            return {}, content
    
    def parse_experiences(self) -> List[ContentItem]:
        about_content = self._read_about_file()
        if not about_content:
            return []
        
        section = self._extract_section(about_content, r'## 💼 Work Experience')
        entries = self._extract_html_blocks(section, 'experience-entry')
        
        items = []
        for entry in entries:
            item = self._parse_experience_entry(entry)
            if item:
                items.append(item)
        
        return sorted(items, key=lambda x: x.date, reverse=True)
    
    def parse_education(self) -> List[ContentItem]:
        about_content = self._read_about_file()
        if not about_content:
            return []
        
        section = self._extract_section(about_content, r'## 🎓 Education')
        entries = self._extract_html_blocks(section, 'education-entry')
        
        items = []
        for entry in entries:
            item = self._parse_education_entry(entry)
            if item:
                items.append(item)
        
        return sorted(items, key=lambda x: x.date, reverse=True)
    
    def parse_certifications(self) -> List[ContentItem]:
        about_content = self._read_about_file()
        if not about_content:
            return []
        
        section = self._extract_section(about_content, r'## 🪪 Certifications & Licenses')
        entries = self._extract_html_blocks(section, 'certification-entry')
        
        items = []
        for entry in entries:
            item = self._parse_certification_entry(entry)
            if item:
                items.append(item)
        
        return sorted(items, key=lambda x: x.date, reverse=True)
    
    def _read_about_file(self) -> str:
        about_path = self.content_root / 'about.md'
        if not about_path.exists():
            return ""
        
        try:
            with open(about_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return ""
    
    def _extract_section(self, content: str, start_pattern: str) -> str:
        start_match = re.search(start_pattern, content)
        if not start_match:
            return ""
        
        section_start = start_match.start()
        next_section = re.search(r'</div>\s*<div class="about-section', content[section_start:])
        
        if next_section:
            section_end = section_start + next_section.start() + len('</div>')
        else:
            section_end = len(content)
        
        return content[section_start:section_end]
    
    def _extract_html_blocks(self, content: str, class_name: str) -> List[str]:
        blocks = []
        pattern = rf'<div class="{class_name}[^"]*">(.*?)</div>(?=\s*(?:<div class="{class_name}|</div>\s*<div class="about-section"|$))'
        matches = re.findall(pattern, content, re.DOTALL)
        return matches
    
    def _parse_experience_entry(self, entry: str) -> Optional[ContentItem]:
        company = self._extract_text(entry, r'### ([^<\n]+)')
        positions = re.findall(r'#### ([^<\n]+)', entry)
        periods = re.findall(r'\*\*Period:\*\* ([^<\n]+)', entry)
        
        if not (company and positions and periods):
            return None
        
        position = self._clean_text(positions[0])
        period = self._clean_text(periods[0])
        
        description_match = re.search(
            rf'#### {re.escape(positions[0])}.*?\*\*Period:\*\* {re.escape(periods[0])}(.*?)(?=#### |---|$)',
            entry, re.DOTALL
        )
        
        description = ""
        if description_match:
            desc_text = description_match.group(1)
            desc_text = re.sub(r'<div class="fields">.*?</div>', '', desc_text, flags=re.DOTALL)
            description = self._extract_description(desc_text, 500)
        
        fields = self._extract_field_tags(entry)
        date_str = self._parse_period_date(period)
        
        unique_id = self._generate_id('experience', f"{company}_{position}_{period}", {})
        
        return ContentItem(
            id=unique_id,
            type='experience',
            title=f"{position} at {company}",
            description=description,
            date=date_str,
            metadata={'company': company, 'position': position, 'period': period},
            fields=fields
        )
    
    def _parse_education_entry(self, entry: str) -> Optional[ContentItem]:
        institution = self._extract_text(entry, r'### ([^<\n]+)')
        degree = self._extract_text(entry, r'#### ([^<\n]+)')
        period = self._extract_text(entry, r'\*\*Period:\*\* ([^<\n]+)')
        
        if not (institution and degree and period):
            return None
        
        desc_match = re.search(r'\*\*Period:\*\* [^<\n]+.*?</div>\s*(.*?)(?=<div class="fields">|$)', 
                              entry, re.DOTALL)
        description = ""
        if desc_match:
            description = self._extract_description(desc_match.group(1), 500)
        
        fields = self._extract_field_tags(entry)
        date_str = self._parse_period_date(period)
        
        unique_id = self._generate_id('education', f"{institution}_{degree}_{period}", {})
        
        return ContentItem(
            id=unique_id,
            type='education',
            title=f"{degree} at {institution}",
            description=description,
            date=date_str,
            metadata={'institution': institution, 'degree': degree, 'period': period},
            fields=fields
        )
    
    def _parse_certification_entry(self, entry: str) -> Optional[ContentItem]:
        title = self._extract_text(entry, r'<h3>([^<]+)</h3>')
        issued = self._extract_text(entry, r'<strong>Issued: ([^<]+)</strong>')
        
        if not (title and issued):
            return None
        
        fields = self._extract_field_tags(entry)
        date_str = self._normalize_date(issued)
        
        unique_id = self._generate_id('certification', f"{title}_{issued}", {})
        
        return ContentItem(
            id=unique_id,
            type='certification',
            title=title,
            description=f"Certification: {title} | Issued: {issued}",
            date=date_str,
            metadata={'title': title, 'issued': issued},
            fields=fields
        )
    
    def _extract_text(self, content: str, pattern: str) -> str:
        match = re.search(pattern, content)
        return self._clean_text(match.group(1)) if match else ""
    
    def _extract_field_tags(self, content: str) -> List[str]:
        fields = re.findall(r'<span class="field-tag">([^<]+)</span>', content)
        return [self._clean_text(field) for field in fields]
    
    def _clean_text(self, text: str) -> str:
        if not text:
            return ""
        
        text = re.sub(r'<[^>]+>', '', text)
        text = html.unescape(text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _extract_description(self, content: str, max_length: int = 400) -> str:
        clean_content = self._clean_text(content)
        
        if len(clean_content) <= max_length:
            return clean_content
        
        truncated = clean_content[:max_length]
        sentence_ends = [truncated.rfind(c) for c in '.!?']
        last_sentence_end = max([pos for pos in sentence_ends if pos > max_length * 0.7], default=-1)
        
        if last_sentence_end > 0:
            return clean_content[:last_sentence_end + 1]
        else:
            return truncated.rstrip() + "..."
    
    def _parse_period_date(self, period: str) -> str:
        if ' - Present' in period:
            start_date = period.split(' - ')[0].strip()
            return self._normalize_date(start_date)
        elif ' - ' in period:
            end_date = period.split(' - ')[1].strip()
            return self._normalize_date(end_date)
        else:
            return self._normalize_date(period)
    
    def _normalize_date(self, date_str: str) -> str:
        if not date_str:
            return datetime.now().strftime('%Y-%m-%d')
        
        date_str = str(date_str).strip()
        
        for pattern, fmt in self.date_patterns:
            if re.match(pattern, date_str):
                try:
                    if fmt == '%b %Y':
                        dt = datetime.strptime(date_str, fmt)
                        return dt.strftime('%Y-%m-%d')
                    elif fmt == '%Y':
                        return f"{date_str}-01-01"
                    else:
                        dt = datetime.strptime(date_str, fmt)
                        return dt.strftime('%Y-%m-%d')
                except ValueError:
                    continue
        
        return datetime.now().strftime('%Y-%m-%d')
    
    def _generate_id(self, content_type: str, identifier: str, metadata: Dict) -> str:
        id_string = f"{content_type}:{identifier}:{str(sorted(metadata.items()))}"
        return hashlib.md5(id_string.encode()).hexdigest()