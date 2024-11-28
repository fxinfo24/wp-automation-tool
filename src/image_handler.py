#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 21:25:30 2024

@author: thesaint
"""

# src/image_handler.py
from PIL import Image
import requests
from io import BytesIO
from typing import Dict, List
import logging
from datetime import datetime
from pathlib import Path

class ImageHandler:
    def __init__(self, config_manager):
        self.unsplash_key = config_manager.get_credentials('unsplash')['access_key']
        self.max_size = (800, 800)  # Maximum image dimensions
        self.image_cache_dir = Path('data/image_cache')
        self.image_cache_dir.mkdir(parents=True, exist_ok=True)
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            filename=f'logs/image_handler_{datetime.now():%Y%m%d}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    async def fetch_images(self, topic: str, count: int = 3) -> List[Dict]:
        try:
            headers = {'Authorization': f'Client-ID {self.unsplash_key}'}
            endpoint = f'https://api.unsplash.com/search/photos?query={topic}&per_page={count}'
            
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            
            images = response.json()['results']
            return [
                {
                    'id': img['id'],
                    'url': img['urls']['raw'],
                    'description': img['description'] or topic,
                    'credit': {
                        'name': img['user']['name'],
                        'link': img['user']['links']['html']
                    }
                }
                for img in images
            ]
        except Exception as e:
            logging.error(f"Failed to fetch images: {str(e)}")
            raise
            
    async def optimize_image(self, image_data: Dict) -> Dict:
        try:
            # Check cache first
            cached_image = self._get_cached_image(image_data['id'])
            if cached_image:
                return cached_image
            
            # Download and process image
            response = requests.get(image_data['url'])
            response.raise_for_status()
            
            img = Image.open(BytesIO(response.content))
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
                
            # Resize image
            img.thumbnail(self.max_size, Image.Resampling.LANCZOS)
            
            # Optimize and save
            output = BytesIO()
            img.save(output, 
                    format='JPEG', 
                    quality=85, 
                    optimize=True)
            
            optimized_data = {
                'id': image_data['id'],
                'data': output.getvalue(),
                'format': 'jpeg',
                'size': img.size,
                'description': image_data['description'],
                'credit': image_data['credit']
            }
            
            # Cache the optimized image
            self._cache_image(optimized_data)
            
            return optimized_data
            
        except Exception as e:
            logging.error(f"Image optimization failed: {str(e)}")
            raise
            
    def _get_cached_image(self, image_id: str) -> Dict:
        cache_file = self.image_cache_dir / f'{image_id}.jpg'
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    return {
                        'id': image_id,
                        'data': f.read(),
                        'format': 'jpeg',
                        'cached': True
                    }
            except Exception as e:
                logging.error(f"Failed to read cached image: {str(e)}")
                return None
        return None
        
    def _cache_image(self, image_data: Dict) -> None:
        try:
            cache_file = self.image_cache_dir / f"{image_data['id']}.jpg"
            with open(cache_file, 'wb') as f:
                f.write(image_data['data'])
            logging.info(f"Image cached successfully: {image_data['id']}")
        except Exception as e:
            logging.error(f"Failed to cache image: {str(e)}")
            
    async def fetch_and_optimize_images(self, topic: str, count: int = 3) -> List[Dict]:
        try:
            images = await self.fetch_images(topic, count)
            optimized_images = []
            
            for img in images:
                optimized = await self.optimize_image(img)
                optimized_images.append(optimized)
                
            return optimized_images
            
        except Exception as e:
            logging.error(f"Fetch and optimize operation failed: {str(e)}")
            raise