#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 18:44:06 2024

@author: thesaint
"""

# src/media_integration.py
from typing import Dict, List, Optional
import logging
from src.image_handler import ImageHandler
from src.video_handler import YouTubeHandler
from src.rate_limiter import RateLimiter

class MediaIntegration:
    def __init__(self, config_manager):
        self.image_handler = ImageHandler(config_manager)
        self.video_handler = YouTubeHandler(config_manager)
        self.rate_limiter = RateLimiter()
        self.setup_logging()
        
    async def process_media(self, topic: str, keywords: List[str]) -> Dict:
        try:
            # Apply rate limiting
            await self.rate_limiter.acquire('unsplash')
            images = await self.image_handler.fetch_images(topic, count=3)
            
            await self.rate_limiter.acquire('youtube')
            video = await self.video_handler.find_relevant_video(keywords[0])
            
            return {
                'featured_image': await self._process_featured_image(images[0] if images else None),
                'content_images': await self._process_content_images(images[1:] if len(images) > 1 else []),
                'video': video,
                'media_status': self._validate_media(images, video)
            }
        except Exception as e:
            logging.error(f"Media processing failed: {str(e)}")
            raise
        finally:
            await self.rate_limiter.release('unsplash')
            await self.rate_limiter.release('youtube')