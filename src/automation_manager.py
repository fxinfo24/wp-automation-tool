#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 21:39:45 2024

@author: thesaint
"""

# src/automation_manager.py
from typing import Dict, List
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from src.content_generator import ContentGenerator
from src.image_handler import ImageHandler
from src.wordpress_poster import WordPressPoster
from src.content_quality import ContentQualityAnalyzer

class AutomationManager:
    def __init__(self, config_manager):
        self.config = config_manager
        self.content_generator = ContentGenerator(config_manager)
        self.image_handler = ImageHandler(config_manager)
        self.wordpress_poster = WordPressPoster(config_manager)
        self.quality_analyzer = ContentQualityAnalyzer()
        self.post_interval = 14 * 60  # 14 minutes in seconds
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            filename=f'logs/automation_manager_{datetime.now():%Y%m%d}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    async def process_batch(self, input_file: str) -> None:
        try:
            topics = self._read_input_file(input_file)
            for topic in topics:
                try:
                    await self._process_single_topic(topic)
                    await asyncio.sleep(self.post_interval)
                except Exception as e:
                    logging.error(f"Failed to process topic {topic['topic']}: {str(e)}")
                    continue
        except Exception as e:
            logging.error(f"Batch processing failed: {str(e)}")
            raise
            
    async def _process_single_topic(self, topic_data: Dict) -> None:
        try:
            # Generate content
            content = await self.content_generator.generate_article(
                topic_data['topic'],
                {
                    'primary': topic_data['primary_keywords'],
                    'secondary': topic_data['additional_keywords'],
                    'audience': topic_data['target_audience'],
                    'tone': topic_data['tone']
                }
            )
            
            # Analyze content quality
            quality_metrics = await self.quality_analyzer.analyze_content(
                content,
                topic_data['primary_keywords']
            )
            
            if not self._meets_quality_standards(quality_metrics):
                logging.warning(f"Content quality below threshold for topic: {topic_data['topic']}")
                return
                
            # Process media
            media = await self._process_media(topic_data)
            
            # Prepare post data
            post_data = {
                'title': topic_data['topic'],
                'content': content,
                'featured_image': media['featured_image'],
                'content_images': media['content_images'],
                'video': media['video'],
                'categories': topic_data.get('categories', []),
                'tags': topic_data.get('tags', []),
                'status': 'publish'
            }
            
            # Create WordPress post
            post_id = await self.wordpress_poster.create_post(post_data)
            logging.info(f"Successfully created post {post_id} for topic: {topic_data['topic']}")
            
            # Record success
            self._record_success(topic_data, post_id, quality_metrics)
            
        except Exception as e:
            logging.error(f"Topic processing failed: {str(e)}")
            raise
            
    async def _process_media(self, topic_data: Dict) -> Dict:
        try:
            images = await self.image_handler.fetch_and_optimize_images(
                topic_data['topic'],
                count=3
            )
            
            video = await self._fetch_relevant_video(
                topic_data['topic'],
                topic_data['primary_keywords']
            )
            
            return {
                'featured_image': images[0] if images else None,
                'content_images': images[1:] if len(images) > 1 else [],
                'video': video
            }
        except Exception as e:
            logging.error(f"Media processing failed: {str(e)}")
            raise
            
    def _meets_quality_standards(self, metrics: Dict) -> bool:
        return (
            metrics['readability_metrics']['readability_score'] > 60 and
            metrics['quality_score'] > 80 and
            metrics['keyword_optimization']['keyword_presence']
        )
        
    def _record_success(self, topic_data: Dict, post_id: str, metrics: Dict) -> None:
        record = {
            'timestamp': datetime.now().isoformat(),
            'topic': topic_data['topic'],
            'post_id': post_id,
            'quality_metrics': metrics
        }
        
        history_dir = Path('data/post_history')
        history_dir.mkdir(exist_ok=True)
        
        with open(history_dir / f'post_{post_id}.json', 'w') as f:
            json.dump(record, f, indent=4)