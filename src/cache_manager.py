#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 18:10:25 2024

@author: thesaint
"""

# src/cache_manager.py
import json
from pathlib import Path
from typing import Dict, Optional
import hashlib
from datetime import datetime

class CacheManager:
    def __init__(self):
        self.cache_dir = Path('data/content_cache')
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def get_cached_content(self, topic: str, keywords: Dict) -> Optional[Dict]:
        cache_key = self._generate_cache_key(topic, keywords)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                cached_data = json.load(f)
                if not self._is_cache_expired(cached_data):
                    return cached_data['content']
        return None
        
    def cache_content(self, topic: str, keywords: Dict, content: Dict) -> None:
        cache_key = self._generate_cache_key(topic, keywords)
        cache_data = {
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'keywords': keywords
        }
        
        cache_file = self.cache_dir / f"{cache_key}.json"
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=4)
            
    def _generate_cache_key(self, topic: str, keywords: Dict) -> str:
        cache_data = f"{topic}_{sorted(keywords.items())}"
        return hashlib.md5(cache_data.encode()).hexdigest()[:12]
        
    def _is_cache_expired(self, cached_data: Dict, max_age_hours: int = 24) -> bool:
        cached_time = datetime.fromisoformat(cached_data['timestamp'])
        age = datetime.now() - cached_time
        return age.total_seconds() > (max_age_hours * 3600)