#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 00:51:22 2024

@author: thesaint
"""

# src/content_management/status_tracker.py
from typing import Dict, List
import json
from pathlib import Path
import logging
from datetime import datetime

class StatusTracker:
    def __init__(self):
        self.status_dir = Path('data/status')
        self.status_dir.mkdir(parents=True, exist_ok=True)
        self.setup_logging()
        
    def setup_logging(self):
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        logging.basicConfig(
            filename=log_dir / f'status_tracker_{datetime.now():%Y%m%d}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    async def track_post(self, post_id: str, status: Dict) -> None:
        try:
            status_data = {
                'post_id': post_id,
                'timestamp': datetime.now().isoformat(),
                'status': status['state'],
                'metrics': {
                    'word_count': status.get('word_count', 0),
                    'image_count': status.get('image_count', 0),
                    'keyword_density': status.get('keyword_density', {}),
                    'processing_time': status.get('processing_time', 0)
                }
            }
            
            await self._save_status(post_id, status_data)
            logging.info(f"Status tracked for post {post_id}: {status['state']}")
            
        except Exception as e:
            logging.error(f"Status tracking failed for post {post_id}: {str(e)}")
            raise
            
    async def _save_status(self, post_id: str, status_data: Dict) -> None:
        status_file = self.status_dir / f'{post_id}.json'
        with open(status_file, 'w') as f:
            json.dump(status_data, f, indent=4)