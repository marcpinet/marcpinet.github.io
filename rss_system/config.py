import os

class Config:
    SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CONTENT_ROOT = os.path.join(SITE_ROOT, 'content')
    OUTPUT_ROOT = os.path.join(SITE_ROOT, 'static')
    RSS_SYSTEM_ROOT = os.path.dirname(os.path.abspath(__file__))
    
    BASE_URL = "https://marcpinet.fr"
    SITE_TITLE = "Marc Pinet"
    
    FEED_TYPES = {
        'posts': {
            'title': 'Posts',
            'description': 'Latest blog posts and articles from Marc Pinet'
        },
        'projects': {
            'title': 'Projects', 
            'description': 'New projects and developments from Marc Pinet'
        },
        'experiences': {
            'title': 'Work Experience',
            'description': 'Latest work experiences and career updates from Marc Pinet'
        },
        'education': {
            'title': 'Education',
            'description': 'Educational achievements and academic updates from Marc Pinet'
        },
        'certifications': {
            'title': 'Certifications',
            'description': 'New certifications and professional achievements from Marc Pinet'
        }
    }
    
    MAX_ENTRIES_PER_FEED = 20
    
    @classmethod
    def get_state_file_path(cls):
        return os.path.join(cls.OUTPUT_ROOT, 'rss_state.json')
    
    @classmethod
    def get_feeds_directory(cls):
        return os.path.join(cls.OUTPUT_ROOT, 'feeds')
    
    @classmethod
    def validate_paths(cls):
        if not os.path.exists(cls.CONTENT_ROOT):
            raise FileNotFoundError(f"Content directory not found: {cls.CONTENT_ROOT}")
        
        os.makedirs(cls.OUTPUT_ROOT, exist_ok=True)
        os.makedirs(cls.get_feeds_directory(), exist_ok=True)
        
        return True