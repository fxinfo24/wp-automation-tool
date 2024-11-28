#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 01:07:24 2024

@author: thesaint
"""

# tests/test_integration_scenarios.py
import pytest
from pathlib import Path

class TestIntegrationScenarios:
    @pytest.mark.asyncio
    async def test_complete_post_workflow(self, automation_manager):
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