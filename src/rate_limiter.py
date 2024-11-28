#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 17:59:02 2024

@author: thesaint
"""

# src/rate_limiter.py
from datetime import datetime, timedelta
import asyncio
import logging
from typing import Dict, List, Optional
from collections import defaultdict, deque
from dataclasses import dataclass

@dataclass
class RateLimit:
    requests_per_minute: int
    requests_per_hour: int
    base_retry_delay: int
    max_retry_attempts: int

class EnhancedRateLimiter:
    def __init__(self):
        # API-specific configurations
        self.api_limits = {
            'openai': RateLimit(20, 1000, 2, 5),
            'unsplash': RateLimit(50, 500, 1, 3),
            'youtube': RateLimit(100, 1000, 1, 3),
            'wordpress': RateLimit(30, 300, 3, 4)
        }
        
        # Request tracking and queuing
        self.request_history = defaultdict(list)
        self.request_queues = {api: deque() for api in self.api_limits.keys()}
        self.quota_warnings = defaultdict(int)
        
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            filename='logs/rate_limiter.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    async def acquire(self, api_name: str, priority: int = 1) -> bool:
        try:
            # Add request to queue
            await self._enqueue_request(api_name, priority)
            
            # Process queue
            while self.request_queues[api_name]:
                if await self._can_process_request(api_name):
                    self.request_queues[api_name].popleft()
                    await self._record_request(api_name)
                    return True
                else:
                    await self._apply_backoff(api_name)
            
            return False
            
        except Exception as e:
            logging.error(f"Rate limiter error for {api_name}: {str(e)}")
            return False

    async def _enqueue_request(self, api_name: str, priority: int) -> None:
        # Priority queue implementation
        self.request_queues[api_name].append((priority, datetime.now()))
        self._monitor_queue_size(api_name)

    async def _can_process_request(self, api_name: str) -> bool:
        current_time = datetime.now()
        await self._clean_history(api_name, current_time)
        
        minute_requests = self._count_recent_requests(api_name, minutes=1)
        hour_requests = len(self.request_history[api_name])
        
        return (minute_requests < self.api_limits[api_name].requests_per_minute and
                hour_requests < self.api_limits[api_name].requests_per_hour)

    async def _apply_backoff(self, api_name: str) -> None:
        attempts = self.quota_warnings[api_name]
        if attempts < self.api_limits[api_name].max_retry_attempts:
            delay = self.api_limits[api_name].base_retry_delay * (2 ** attempts)
            self.quota_warnings[api_name] += 1
            logging.warning(f"{api_name} rate limit backoff: {delay}s")
            await asyncio.sleep(delay)
        else:
            raise Exception(f"Max retry attempts reached for {api_name}")

    async def _record_request(self, api_name: str) -> None:
        self.request_history[api_name].append(datetime.now())
        self._update_quota_status(api_name)

    def _update_quota_status(self, api_name: str) -> None:
        hour_usage = len(self.request_history[api_name])
        hour_limit = self.api_limits[api_name].requests_per_hour
        
        usage_percentage = (hour_usage / hour_limit) * 100
        if usage_percentage >= 80:
            logging.warning(f"{api_name} quota usage at {usage_percentage:.1f}%")

    def _monitor_queue_size(self, api_name: str) -> None:
        queue_size = len(self.request_queues[api_name])
        if queue_size > 100:  # Arbitrary threshold
            logging.warning(f"Large queue size for {api_name}: {queue_size} requests")

    async def get_status(self, api_name: str) -> Dict:
        return {
            'queue_size': len(self.request_queues[api_name]),
            'hour_usage': len(self.request_history[api_name]),
            'minute_usage': self._count_recent_requests(api_name, minutes=1),
            'quota_warnings': self.quota_warnings[api_name]
        }

    def _count_recent_requests(self, api_name: str, minutes: int) -> int:
        cutoff = datetime.now() - timedelta(minutes=minutes)
        return sum(1 for time in self.request_history[api_name] if time > cutoff)