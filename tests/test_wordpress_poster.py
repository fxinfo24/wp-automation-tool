#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 00:56:09 2024

@author: thesaint
"""

# tests/test_wordpress_poster.py
import pytest
from src.wordpress_poster import WordPressPoster
from unittest.mock import Mock, patch

class TestWordPressPoster:
    @pytest.fixture
    def config_manager(self):
        mock_config = Mock()
        mock_config.get_credentials.return_value = {
            'url': 'test_url',
            'username': 'test_user',
            'password': 'test_pass'
        }
        return mock_config
        
    @pytest.mark.asyncio
    async def test_create_post(self, config_manager):
        poster = WordPressPoster(config_manager)
        content = {
            'title': 'Test Post',
            'content': 'Test content',
            'featured_image': {'data': b'test', 'id': 'test_id'},
            'categories': ['test_category'],
            'tags': ['test_tag']
        }
        
        with patch('wordpress_xmlrpc.Client') as mock_client:
            mock_client.return_value.call.return_value = '123'
            post_id = await poster.create_post(content)
            assert post_id == '123'