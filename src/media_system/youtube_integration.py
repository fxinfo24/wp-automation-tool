#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 00:45:01 2024

@author: thesaint
"""

# src/media_system/youtube_integration.py
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

class YouTubeIntegrator:
    def __init__(self, config_manager):
        self.api_key = config_manager.get_credentials('youtube')['api_key']
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.max_results = 5  # Number of videos to search
        self.setup_logging()
        
    def setup_logging(self):
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            filename=log_dir / f'youtube_integration_{datetime.now():%Y%m%d}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    async def find_relevant_video(self, topic: str, keywords: List[str]) -> Optional[Dict]:
        try:
            search_response = await self._search_videos(topic, keywords)
            if not search_response.get('items'):
                logging.warning(f"No videos found for topic: {topic}")
                return None
                
            video = await self._select_best_match(search_response['items'], keywords)
            if not video:
                return None
                
            return {
                'video_id': video['id']['videoId'],
                'title': video['snippet']['title'],
                'description': video['snippet']['description'],
                'embed_code': self._generate_embed_code(video['id']['videoId']),
                'thumbnail': video['snippet']['thumbnails']['high']['url']
            }
            
        except HttpError as e:
            logging.error(f"YouTube API error: {str(e)}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error in YouTube integration: {str(e)}")
            return None
            
    async def _search_videos(self, topic: str, keywords: List[str]) -> Dict:
        search_query = f"{topic} {' '.join(keywords)}"
        try:
            return self.youtube.search().list(
                q=search_query,
                part='snippet',
                type='video',
                maxResults=self.max_results,
                videoEmbeddable='true',
                videoSyndicated='true',
                safeSearch='strict'
            ).execute()
        except Exception as e:
            logging.error(f"Video search failed: {str(e)}")
            raise
            
    async def _select_best_match(self, videos: List[Dict], keywords: List[str]) -> Optional[Dict]:
        try:
            scored_videos = []
            for video in videos:
                score = self._calculate_relevance_score(video, keywords)
                scored_videos.append((score, video))
                
            if not scored_videos:
                return None
                
            # Sort by score and return the best match
            return max(scored_videos, key=lambda x: x[0])[1]
            
        except Exception as e:
            logging.error(f"Video selection failed: {str(e)}")
            return None
            
    def _calculate_relevance_score(self, video: Dict, keywords: List[str]) -> float:
        score = 0
        title = video['snippet']['title'].lower()
        description = video['snippet']['description'].lower()
        
        # Score based on keyword presence
        for keyword in keywords:
            keyword = keyword.lower()
            if keyword in title:
                score += 2
            if keyword in description:
                score += 1
                
        return score
        
    def _generate_embed_code(self, video_id: str) -> str:
        return f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>'