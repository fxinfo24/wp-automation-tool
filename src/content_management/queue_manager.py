#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 00:50:40 2024

@author: thesaint
"""

# src/content_management/queue_manager.py
from typing import Dict, List, Optional
import asyncio
from collections import deque
import logging
from datetime import datetime
from pathlib import Path

class QueueManager:
    def __init__(self):
        self.post_queue = deque()
        self.processing = False
        self.setup_logging()
        
    def setup_logging(self):
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        logging.basicConfig(
            filename=log_dir / f'queue_manager_{datetime.now():%Y%m%d}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    async def add_to_queue(self, post_data: Dict) -> None:
        try:
            self.post_queue.append({
                'data': post_data,
                'timestamp': datetime.now(),
                'status': 'queued',
                'retries': 0
            })
            logging.info(f"Added post to queue: {post_data.get('topic', 'Unknown topic')}")
            
            if not self.processing:
                await self.process_queue()
                
        except Exception as e:
            logging.error(f"Failed to add post to queue: {str(e)}")
            raise