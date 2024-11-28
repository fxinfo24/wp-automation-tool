#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 18:38:30 2024

@author: thesaint
"""

# src/post_scheduler.py
import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict

class PostScheduler:
    def __init__(self, config_manager):
        self.config = config_manager
        self.interval_minutes = 14
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            filename='logs/post_scheduler.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    async def schedule_posts(self, posts: List[Dict]) -> None:
        try:
            for index, post in enumerate(posts):
                if index > 0:
                    await self._wait_interval()
                
                logging.info(f"Processing post {index + 1}/{len(posts)}")
                yield post
                
        except Exception as e:
            logging.error(f"Post scheduling failed: {str(e)}")
            raise
    
    async def _wait_interval(self) -> None:
        await asyncio.sleep(self.interval_minutes * 60)