#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 01:43:05 2024

@author: thesaint
"""

# src/content_management/bulk_processor.py
from typing import Dict, List
import asyncio
import logging
from datetime import datetime
from pathlib import Path

class BulkProcessor:
    def __init__(self, automation_manager):
        self.automation_manager = automation_manager
        self.max_concurrent = 3
        self.setup_logging()
        
    def setup_logging(self):
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        logging.basicConfig(
            filename=log_dir / f'bulk_processor_{datetime.now():%Y%m%d}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    async def process_batch(self, topics: List[Dict]) -> List[Dict]:
        try:
            results = []
            for i in range(0, len(topics), self.max_concurrent):
                batch = topics[i:i + self.max_concurrent]
                batch_results = await asyncio.gather(
                    *[self.automation_manager.process_topic(topic) for topic in batch],
                    return_exceptions=True
                )
                results.extend(self._handle_batch_results(batch_results))
                await asyncio.sleep(14 * 60)  # 14-minute interval
            return results
        except Exception as e:
            logging.error(f"Bulk processing failed: {str(e)}")
            raise