#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 18:11:00 2024

@author: thesaint
"""

# src/youtube_handler.py
from googleapiclient.discovery import build
from typing import Optional, Dict
import logging

class YouTubeHandler:
    def __init__(self, config_manager):
        self.api_key = config_manager.get_credentials('youtube')['api_key']
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        
    async def find_relevant_video(self, topic: str, max_results: int = 3) -> Optional[Dict]:
        try:
            search_response = await self._search_videos(topic, max_results)
            if not search_response.get('items'):
                return None
                
            videos = []
            for item in search_response['items']:
                video_id = item['id']['videoId']
                videos.append({
                    'id': video_id,
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'embed_code': self._generate_embed_code(video_id)
                })
            
            return self._select_best_match(videos, topic)
            
        except Exception as e:
            logging.error(f"YouTube video search failed: {str(e)}")
            return None
            
    async def _search_videos(self, topic: str, max_results: int) -> Dict:
        return self.youtube.search().list(
            q=topic,
            part='snippet',
            type='video',
            maxResults=max_results,
            videoEmbeddable='true',
            videoSyndicated='true'
        ).execute()
        
    def _generate_embed_code(self, video_id: str) -> str:
        return f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>'
        
    def _select_best_match(self, videos: List[Dict], topic: str) -> Dict:
        # Implement relevance scoring logic here
        return videos[0] if videos else None