#!/usr/bin/env python3

# tests/integration/test_automation_manager.py
import pytest
from unittest.mock import patch
from src.automation_manager import AutomationManager

class TestAutomationManager:
    @pytest.fixture
    async def automation_manager(self, config_manager):
        manager = AutomationManager(config_manager)
        return manager

    @pytest.mark.asyncio
    async def test_process_batch(self, automation_manager):
        test_topics = [{
            'topic': 'Test Topic',
            'primary_keywords': ['test', 'keywords'],
            'additional_keywords': ['more', 'keywords'],
            'target_audience': 'testers',
            'tone': 'professional'
        }]
        
        with patch('src.content_generator.EnhancedContentGenerator.generate_article') as mock_generate:
            mock_generate.return_value = "Test content"
            result = await automation_manager.process_batch(test_topics)
            assert result is not None

    @pytest.mark.asyncio
    async def test_process_single_topic(self, automation_manager):
        test_topic = {
            'topic': 'Test Topic',
            'primary_keywords': ['test'],
            'additional_keywords': ['more'],
            'target_audience': 'testers',
            'tone': 'professional'
        }
        
        with patch('src.content_generator.EnhancedContentGenerator.generate_article') as mock_generate:
            mock_generate.return_value = "Test content"
            result = await automation_manager._process_single_topic(test_topic)
            assert result is not None