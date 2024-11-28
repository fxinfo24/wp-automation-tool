#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 00:54:52 2024

@author: thesaint
"""

# tests/test_content_generator.py
import pytest
from src.content_generator import ContentGenerator
from unittest.mock import Mock, patch

class TestContentGenerator:
    @pytest.fixture
    def config_manager(self):
        mock_config = Mock()
        mock_config.get_credentials.return_value = {
            'api_key': 'test_key',
            'model': 'gpt-4',
            'temperature': 0.9
        }
        return mock_config
        
    @pytest.mark.asyncio
    async def test_generate_article(self, config_manager):
        generator = ContentGenerator(config_manager)
        topic = "Organic Gardening"
        keywords = {
            'primary': ['organic gardening tips'],
            'secondary': ['sustainable farming'],
            'audience': 'beginners',
            'tone': 'friendly'
        }
        
        with patch('openai.OpenAI') as mock_openai:
            mock_openai.return_value.chat.completions.create.return_value.choices[0].message.content = "Test content"
            content = await generator.generate_article(topic, keywords)
            assert content is not None
            assert len(content) > 0