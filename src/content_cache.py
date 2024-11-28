#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 19:25:39 2024

@author: thesaint
"""

# src/content_cache.py
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

class ContentCache:
    def __init__(self):
        self.cache_dir = Path('data/content_cache')
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_duration = timedelta(days=7)
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            filename='logs/content_cache.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    async def get_cached_content(self, topic: str, keywords: List[str], gpt_version: str) -> Optional[Dict]:
        try:
            cache_key = self._generate_cache_key(topic, keywords, gpt_version)
            cache_file = self.cache_dir / f'{cache_key}.json'
            
            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                    cached_time = datetime.fromisoformat(cached_data['timestamp'])
                    
                    if datetime.now() - cached_time <= self.cache_duration:
                        logging.info(f"Cache hit for topic: {topic}")
                        return cached_data['content']
                    
            logging.info(f"Cache miss for topic: {topic}")
            return None
            
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logging.error(f"Error reading cache: {str(e)}")
            return None
        
    async def cache_content(self, topic: str, keywords: List[str], content: Dict, gpt_version: str) -> None:
        try:
            cache_key = self._generate_cache_key(topic, keywords, gpt_version)
            cache_data = {
                'content': content,
                'timestamp': datetime.now().isoformat(),
                'gpt_version': gpt_version,
                'keywords': keywords
            }
            
            cache_file = self.cache_dir / f'{cache_key}.json'
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=4, ensure_ascii=False)
                
            logging.info(f"Content cached successfully for topic: {topic}")
            
        except Exception as e:
            logging.error(f"Failed to cache content: {str(e)}")
            raise
            
    def _generate_cache_key(self, topic: str, keywords: List[str], gpt_version: str) -> str:
        # Create a unique string combining all relevant data
        cache_string = f"{topic}_{'-'.join(sorted(keywords))}_{gpt_version}"
        # Generate MD5 hash for the cache key
        return hashlib.md5(cache_string.encode('utf-8')).hexdigest()[:12]
        
    def clear_expired_cache(self) -> None:
        try:
            current_time = datetime.now()
            for cache_file in self.cache_dir.glob('*.json'):
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                    cached_time = datetime.fromisoformat(cached_data['timestamp'])
                    
                    if current_time - cached_time > self.cache_duration:
                        cache_file.unlink()
                        logging.info(f"Removed expired cache file: {cache_file.name}")
                        
        except Exception as e:
            logging.error(f"Error clearing expired cache: {str(e)}")