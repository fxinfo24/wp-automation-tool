#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 18:14:16 2024

@author: thesaint
"""

# src/api_fallback.py
from typing import Dict, Optional
import logging
import asyncio

class APIFallbackSystem:
    def __init__(self):
        self.fallback_configs = {
            'openai': {
                'primary': {'model': 'gpt-4', 'temperature': 0.9},
                'fallback': {'model': 'gpt-3.5-turbo', 'temperature': 0.9}
            },
            'image': {
                'primary': 'unsplash',
                'fallback': 'pexels'
            },
            'video': {
                'primary': 'youtube',
                'fallback': 'vimeo'
            }
        }
        
    async def execute_with_fallback(self, api_type: str, operation: callable, *args, **kwargs) -> Optional[Dict]:
        try:
            # Try primary API
            result = await operation(*args, **kwargs)
            if result:
                return result
                
            # If primary fails, try fallback
            if api_type in self.fallback_configs:
                fallback_config = self.fallback_configs[api_type]['fallback']
                kwargs.update({'config': fallback_config})
                return await operation(*args, **kwargs)
                
        except Exception as e:
            logging.error(f"API operation failed with fallback: {str(e)}")
            return None