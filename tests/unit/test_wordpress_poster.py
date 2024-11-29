#!/usr/bin/env python3

# tests/unit/test_wordpress_poster.py
import pytest
from unittest.mock import patch, Mock
from src.wordpress_poster import WordPressPoster

class TestWordPressPoster:
    @pytest.fixture
    async def wordpress_poster(self, config_manager):
        return WordPressPoster(config_manager)

    @pytest.mark.asyncio
    async def test_create_post(self, wordpress_poster):
        test_content = {
            'title': 'Test Post',
            'content': 'Test content',
            'featured_image': {'url': 'test.jpg', 'alt': 'Test Image'},
            'categories': ['test'],
            'tags': ['test']
        }
        
        with patch('wordpress_xmlrpc.Client') as mock_client:
            mock_client.return_value.call.return_value = 123
            post_id = await wordpress_poster.create_post(test_content)
            assert isinstance(post_id, int)

    @pytest.mark.asyncio
    async def test_media_upload(self, wordpress_poster):
        with patch('wordpress_xmlrpc.Client') as mock_client:
            mock_client.return_value.call.return_value = {'id': 456}
            result = await wordpress_poster.upload_media({
                'url': 'test.jpg',
                'alt': 'Test Image'
            })
            assert result['id'] == 456