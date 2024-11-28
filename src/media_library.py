#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 20:08:55 2024

@author: thesaint
"""

# src/media_library.py
from pathlib import Path
from typing import Dict, List
import logging

class MediaLibraryManager:
    def __init__(self, wordpress_handler):
        self.wp = wordpress_handler
        self.media_dir = Path('data/media')
        self.media_dir.mkdir(parents=True, exist_ok=True)
        
    async def process_post_media(self, content: Dict) -> Dict:
        try:
            # Handle featured image
            if content.get('featured_image'):
                featured_id = await self.wp.upload_media(
                    content['featured_image']['optimized_data'],
                    'featured-image.jpg'
                )
                content['featured_image_id'] = featured_id
            
            # Handle content images
            if content.get('content_images'):
                content['image_ids'] = []
                for idx, img in enumerate(content['content_images']):
                    image_id = await self.wp.upload_media(
                        img['optimized_data'],
                        f'content-image-{idx}.jpg'
                    )
                    content['image_ids'].append(image_id)
            
            return content
        except Exception as e:
            logging.error(f"Media library processing failed: {str(e)}")
            raise