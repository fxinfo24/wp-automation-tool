#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 00:55:35 2024

@author: thesaint
"""

# tests/test_image_handler.py
import pytest
from src.image_handler import ImageHandler
from unittest.mock import Mock, patch

class TestImageHandler:
    @pytest.fixture
    def config_manager(self):
        mock_config = Mock()
        mock_config.get_credentials.return_value = {
            'access_key': 'test_key'
        }
        return mock_config
        
    @pytest.mark.asyncio
    async def test_fetch_images(self, config_manager):
        handler = ImageHandler(config_manager)
        topic = "Organic Gardening"
        
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = {
                'results': [
                    {
                        'id': 'test1',
                        'urls': {'raw': 'test_url'},
                        'description': 'test description',
                        'user': {'name': 'test user', 'links': {'html': 'test_link'}}
                    }
                ]
            }
            images = await handler.fetch_images(topic)
            assert len(images) > 0
            assert 'url' in images[0]