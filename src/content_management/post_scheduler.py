#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 00:49:43 2024

@author: thesaint
"""

# src/content_management/post_scheduler.py
from typing import Dict, List
import asyncio
import logging
from datetime import datetime, timedelta
from pathlib import Path

class PostScheduler:
    def __init__(self, config_manager):
        self.config = config_manager
        self.interval_minutes = 14
        self.max_daily_posts = 100
        self.post_queue = []
        self.setup_logging()
        
    def setup_logging(self):
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        logging.basicConfig(
            filename=log_dir / f'post_scheduler_{datetime.now():%Y%m%d}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    async def schedule_posts(self, posts: List[Dict]) -> None:
        try:
            for index, post in enumerate(posts):
                if index >= self.max_daily_posts:
                    logging.warning("Daily post limit reached")
                    break
                    
                await self._process_post(post)
                if index < len(posts) - 1:
                    await self._wait_interval()
                    
        except Exception as e:
            logging.error(f"Post scheduling failed: {str(e)}")
            raise
            
    async def _process_post(self, post: Dict) -> None:
        try:
            post_id = await self._create_post(post)
            await self._update_status(post_id, 'published')
            logging.info(f"Successfully published post: {post_id}")
        except Exception as e:
            logging.error(f"Post processing failed: {str(e)}")
            raise
            
    async def _wait_interval(self) -> None:
        logging.info(f"Waiting {self.interval_minutes} minutes before next post")
        await asyncio.sleep(self.interval_minutes * 60)