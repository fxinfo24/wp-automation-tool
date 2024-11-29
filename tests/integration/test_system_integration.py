#!/usr/bin/env python3

# tests/integration/test_system_integration.py

import pytest
from unittest.mock import patch
from src.automation_manager import AutomationManager

class TestSystemIntegration:
    @pytest.fixture
    async def automation_system(self, config_manager):
        return AutomationManager(config_manager)

    @pytest.mark.asyncio
    async def test_full_workflow(self, automation_system):
        test_topic = {
            'topic': 'Integration Test',
            'primary_keywords': ['test'],
            'additional_keywords': ['integration'],
            'target_audience': 'developers',
            'tone': 'technical',
            'word_count': 3200
        }
        
        with patch('src.content_generator.EnhancedContentGenerator.generate_article', return_value="Test content"):
            with patch('src.image_handler.ImageHandler.fetch_and_optimize_images', return_value=[{'url': 'test.jpg'}]):
                with patch('src.wordpress_poster.WordPressPoster.create_post', return_value=123):
                    result = await automation_system._process_single_topic(test_topic)
                    assert result is not None
                    assert 'post_id' in result

    @pytest.mark.asyncio
    async def test_error_recovery(self, automation_system):
        test_topic = {
            'topic': 'Error Test',
            'primary_keywords': ['test'],
            'word_count': 3200
        }
        
        with patch('src.content_generator.EnhancedContentGenerator.generate_article', side_effect=Exception("API Error")):
            with pytest.raises(Exception):
                await automation_system._process_single_topic(test_topic)