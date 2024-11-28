#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 00:35:55 2024

@author: thesaint
"""

# src/media_system/media_library.py
from typing import Dict, List
import logging
from pathlib import Path
import json

class MediaLibrary:
    def __init__(self, wordpress_handler):
        self.wp = wordpress_handler
        self.media_dir = Path('data/media')
        self.media_dir.mkdir(parents=True, exist_ok=True)
        self.setup_logging()
        
    async def process_post_media(self, content: Dict) -> Dict:
        try:
            processed_content = content.copy()
            
            # Handle featured image
            if content.get('featured_image'):
                featured_id = await self.wp.upload_media(
                    content['featured_image']['data'],
                    f"featured-{content['featured_image']['id']}.jpg"
                )
                processed_content['featured_image_id'] = featured_id
                
            # Handle content images
            if content.get('content_images'):
                processed_content['image_ids'] = []
                for img in content['content_images']:
                    image_id = await self.wp.upload_media(
                        img['data'],
                        f"content-{img['id']}.jpg"
                    )
                    processed_content['image_ids'].append(image_id)
                    
            return processed_content
            
        except Exception as e:
            logging.error(f"Media library processing failed: {str(e)}")
            raise