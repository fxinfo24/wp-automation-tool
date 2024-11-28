#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 01:11:28 2024

@author: thesaint
"""

# tests/test_error_handling.py
import pytest
import asyncio
from unittest.mock import Mock, patch
from src.automation_manager import AutomationManager
from src.content_generator import ContentGenerator
from src.image_handler import ImageHandler

class TestErrorHandling:
    @pytest.fixture
    async def automation_manager(self, config_manager):
        return AutomationManager(config_manager)

    @pytest.mark.asyncio
    async def test_invalid_api_key_handling(self, automation_manager):
        with pytest.raises(Exception) as exc_info:
            with patch.dict(automation_manager.config.credentials['openai'], {'api_key': 'invalid_key'}):
                await automation_manager.content_generator.generate_article(
                    topic='Test Topic',
                    keywords={
                        'primary': ['test keyword'],
                        'secondary': ['additional test'],
                        'audience': 'testers',
                        'tone': 'technical'
                    }
                )
        assert 'Authentication' in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_rate_limit_handling(self, automation_manager):
        test_data = {
            'topic': 'Rate Limit Test',
            'primary_keywords': ['test'],
            'additional_keywords': ['testing'],
            'target_audience': 'testers',
            'tone': 'technical',
            'word_count': 3200
        }

        # Simulate multiple concurrent requests
        async def process_request():
            return await automation_manager.process_topic(test_data)

        tasks = [process_request() for _ in range(5)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Check if rate limiting was applied
        rate_limit_errors = [r for r in results if isinstance(r, Exception) and 'rate limit' in str(r).lower()]
        assert len(rate_limit_errors) > 0

    @pytest.mark.asyncio
    async def test_image_fetch_failure(self, automation_manager):
        with patch('src.image_handler.ImageHandler.fetch_images') as mock_fetch:
            mock_fetch.side_effect = Exception('Image service unavailable')
            
            result = await automation_manager.process_topic({
                'topic': 'Test Topic',
                'primary_keywords': ['test'],
                'word_count': 3200
            })
            
            assert result.get('status') == 'partial_success'
            assert 'image_error' in result.get('errors', [])

    @pytest.mark.asyncio
    async def test_wordpress_connection_error(self, automation_manager):
        with patch('src.wordpress_poster.WordPressPoster.create_post') as mock_post:
            mock_post.side_effect = Exception('WordPress connection failed')
            
            with pytest.raises(Exception) as exc_info:
                await automation_manager.process_topic({
                    'topic': 'Test Topic',
                    'primary_keywords': ['test'],
                    'word_count': 3200
                })
            
            assert 'WordPress connection failed' in str(exc_info.value)