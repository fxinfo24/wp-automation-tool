#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 02:02:57 2024

@author: thesaint
"""

# tests/test_integration.py
import pytest
from src.automation_manager import AutomationManager
from src.content_generator import ContentGenerator
from src.image_handler import ImageHandler
from src.wordpress_poster import WordPressPoster

class TestIntegration:
    @pytest.fixture
    async def automation_manager(self, config_manager):
        return AutomationManager(config_manager)
    
    @pytest.mark.asyncio
    async def test_complete_workflow(self, automation_manager):
        test_data = {
            'topic': 'Integration Test',
            'primary_keywords': ['integration testing'],
            'additional_keywords': ['automation testing'],
            'target_audience': 'developers',
            'tone': 'technical',
            'word_count': 3200,
            'gpt_version': '4'
        }
        
        result = await automation_manager.process_topic(test_data)
        assert result['post_id'] is not None
        assert result['status'] == 'published'
        assert len(result['media_ids']) >= 2