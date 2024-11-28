#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 18:13:40 2024

@author: thesaint
"""

# src/monitoring_dashboard.py
from datetime import datetime
import logging
from typing import Dict, List
import psutil
import json

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            'api_calls': {},
            'content_generation': [],
            'media_processing': [],
            'wordpress_posting': []
        }
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            filename=f'logs/performance_{datetime.now():%Y%m%d}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    async def track_operation(self, operation_type: str, duration: float, status: str):
        try:
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'duration': duration,
                'status': status,
                'memory_usage': psutil.Process().memory_info().rss,
                'cpu_percent': psutil.cpu_percent()
            }
            
            self.metrics[operation_type].append(metrics)
            self._save_metrics()
            
        except Exception as e:
            logging.error(f"Performance tracking failed: {str(e)}")
            
    def _save_metrics(self):
        try:
            with open('logs/performance_metrics.json', 'w') as f:
                json.dump(self.metrics, f, indent=4)
        except Exception as e:
            logging.error(f"Failed to save metrics: {str(e)}")