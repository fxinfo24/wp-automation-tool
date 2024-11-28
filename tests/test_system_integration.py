#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 02:14:29 2024

@author: thesaint
"""

# tests/test_system_integration.py
import pytest
from src.automation_manager import AutomationManager

class TestSystemIntegration:
    @pytest.fixture
    async def automation_manager(self, config_manager):
        return AutomationManager(config_manager)
        
    @pytest.mark.integration
    async def test_end_to_end_flow(self, automation_manager):
        test_data = {
            'topic': 'System Integration Test',
            'primary_keywords': ['system testing'],
            'additional_keywords': ['integration testing'],
            'target_audience': 'developers',
            'tone': 'technical',
            'word_count': 3200,
            'gpt_version': '4'
        }
        
        result = await automation_manager.process_topic(test_data)
        assert result['status'] == 'published'
        assert result['word_count'] >= 3200
        assert len(result['media_ids']) >= 3