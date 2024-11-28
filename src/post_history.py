#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 19:18:42 2024

@author: thesaint
"""

# src/post_history.py
from datetime import datetime
import json
from pathlib import Path
from typing import Dict, List

class PostHistoryManager:
    def __init__(self):
        self.history_dir = Path('data/post_history')
        self.history_dir.mkdir(parents=True, exist_ok=True)
        
    async def record_post(self, post_data: Dict) -> None:
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            history_file = self.history_dir / f'post_{timestamp}.json'
            
            post_record = {
                'timestamp': datetime.now().isoformat(),
                'post_id': post_data.get('id'),
                'title': post_data.get('title'),
                'keywords': post_data.get('keywords'),
                'media_info': post_data.get('media'),
                'status': post_data.get('status'),
                'gpt_version': post_data.get('gpt_version'),
                'word_count': post_data.get('word_count')
            }
            
            with open(history_file, 'w') as f:
                json.dump(post_record, f, indent=4)
                
        except Exception as e:
            logging.error(f"Failed to record post history: {str(e)}")
            raise