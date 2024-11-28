#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 01:57:23 2024

@author: thesaint
"""

# src/performance_monitor.py
import time
import psutil
import logging
from datetime import datetime
from typing import Dict, List
from pathlib import Path

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            'api_calls': {
                'openai': [],
                'unsplash': [],
                'youtube': [],
                'wordpress': []
            },
            'operations': {
                'content_generation': [],
                'media_processing': [],
                'post_creation': [],
                'bulk_processing': []
            },
            'system_resources': []
        }
        self.setup_logging()
        
    def setup_logging(self):
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        logging.basicConfig(
            filename=log_dir / f'performance_{datetime.now():%Y%m%d}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    async def track_operation(self, operation_type: str):
        def decorator(func):
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                start_memory = psutil.Process().memory_info().rss
                
                try:
                    result = await func(*args, **kwargs)
                    self._record_metrics(operation_type, start_time, start_memory)
                    return result
                except Exception as e:
                    self._record_error(operation_type, str(e))
                    raise
                    
            return wrapper
        return decorator
        
    def _record_metrics(self, operation_type: str, start_time: float, start_memory: int) -> None:
        duration = time.time() - start_time
        memory_used = psutil.Process().memory_info().rss - start_memory
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'duration': duration,
            'memory_used': memory_used / (1024 * 1024),  # Convert to MB
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent
        }
        
        if operation_type.startswith('api_'):
            service = operation_type.split('_')[1]
            self.metrics['api_calls'][service].append(metrics)
        else:
            self.metrics['operations'][operation_type].append(metrics)
            
        self.metrics['system_resources'].append({
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent
        })
        
        logging.info(f"Performance metrics recorded for {operation_type}: Duration={duration:.2f}s, Memory={memory_used/1024/1024:.2f}MB")
        
    def _record_error(self, operation_type: str, error_message: str) -> None:
        logging.error(f"Error in {operation_type}: {error_message}")
        
    async def get_performance_report(self) -> Dict:
        return {
            'api_performance': self._calculate_api_metrics(),
            'operation_performance': self._calculate_operation_metrics(),
            'system_health': self._calculate_system_metrics()
        }
        
    def _calculate_api_metrics(self) -> Dict:
        return {
            service: {
                'total_calls': len(calls),
                'avg_duration': sum(c['duration'] for c in calls) / len(calls) if calls else 0,
                'avg_memory': sum(c['memory_used'] for c in calls) / len(calls) if calls else 0
            }
            for service, calls in self.metrics['api_calls'].items()
        }