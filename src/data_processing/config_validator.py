#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 00:03:17 2024

@author: thesaint
"""

# src/data_processing/config_validator.py
from typing import Dict
import logging
import re

class ConfigValidator:
    def __init__(self):
        # Initialize any necessary attributes here
        logging.basicConfig(level=logging.INFO)

    async def _validate_api_keys(self, config: Dict) -> None:
        try:
            # OpenAI API key validation
            if 'openai' in config:
                openai_key = config['openai']['api_key']
                if not re.match(r'^sk-[A-Za-z0-9]{48}$', openai_key):
                    raise ValueError("Invalid OpenAI API key format")
                    
            # WordPress credentials validation
            if 'wordpress' in config:
                wp_url = config['wordpress']['url']
                if not wp_url.startswith(('http://', 'https://')):
                    raise ValueError("Invalid WordPress URL format")
                    
            # Unsplash API key validation
            if 'unsplash' in config:
                unsplash_key = config['unsplash']['access_key']
                if not re.match(r'^[A-Za-z0-9-_]{32}$', unsplash_key):
                    raise ValueError("Invalid Unsplash access key format")
                    
            # YouTube API key validation
            if 'youtube' in config:
                youtube_key = config['youtube']['api_key']
                if not re.match(r'^[A-Za-z0-9-_]{39}$', youtube_key):
                    raise ValueError("Invalid YouTube API key format")
                    
            logging.info("API key validation successful")
            
        except Exception as e:
            logging.error(f"API key validation failed: {str(e)}")
            raise
            
    async def _validate_rate_limits(self, config: Dict) -> None:
        try:
            rate_limits = {
                'openai': {
                    'requests_per_minute': 20,
                    'requests_per_hour': 1000
                },
                'unsplash': {
                    'requests_per_hour': 50
                },
                'youtube': {
                    'requests_per_day': 10000
                },
                'wordpress': {
                    'posts_per_hour': 30
                }
            }
            
            for service, limits in rate_limits.items():
                if service in config:
                    service_config = config[service]
                    for limit_type, limit_value in limits.items():
                        if limit_type in service_config:
                            if int(service_config[limit_type]) > limit_value:
                                raise ValueError(
                                    f"Rate limit for {service} {limit_type} "
                                    f"exceeds maximum allowed: {limit_value}"
                                )
                                
            logging.info("Rate limit validation successful")
            
        except Exception as e:
            logging.error(f"Rate limit validation failed: {str(e)}")
            raise