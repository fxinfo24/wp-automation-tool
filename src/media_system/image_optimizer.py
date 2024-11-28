#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 00:35:01 2024

@author: thesaint
"""

# src/media_system/image_optimizer.py
from PIL import Image
from io import BytesIO
import logging
from typing import Dict, List
from pathlib import Path

class ImageOptimizer:
    def __init__(self):
        self.max_size = (800, 800)
        self.quality = 85
        self.cache_dir = Path('data/image_cache')
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.setup_logging()
        
    async def optimize_image(self, image_data: bytes, image_id: str) -> Dict:
        try:
            # Check cache first
            cached_image = self._get_cached_image(image_id)
            if cached_image:
                return cached_image
                
            # Process new image
            img = Image.open(BytesIO(image_data))
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
                
            # Resize and optimize
            img.thumbnail(self.max_size, Image.Resampling.LANCZOS)
            optimized = BytesIO()
            img.save(optimized, 
                    format='JPEG', 
                    quality=self.quality, 
                    optimize=True)
                    
            return {
                'id': image_id,
                'data': optimized.getvalue(),
                'format': 'jpeg',
                'size': img.size
            }
            
        except Exception as e:
            logging.error(f"Image optimization failed: {str(e)}")
            raise