#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 19:37:08 2024

@author: thesaint
"""

# src/video_handler.py
from googleapiclient.discovery import build
import logging
from typing import Dict, Optional

class YouTubeHandler:
    def __init__(self, config_manager):
        self.api_key = config_manager.get_credentials('youtube')['api_key']
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        
    async def find_relevant_video(self, topic: str) -> Optional[Dict]:
        try:
            search_response = await self._search_videos(topic)
            if not search_response.get('items'):
                return None
                
            video_id = search_response['items'][0]['id']['videoId']
            return {
                'embed_code': self._generate_embed_code(video_id),
                'video_id': video_id,
                'title': search_response['items'][0]['snippet']['title']
            }
        except Exception as e:
            logging.error(f"YouTube video search failed: {str(e)}")
            return None
            
    def _generate_embed_code(self, video_id: str) -> str:
        return f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>'