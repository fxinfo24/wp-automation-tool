#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 00:59:47 2024

@author: thesaint
"""

# tests/test_error_scenarios.py
import pytest
from src.content_generator import ContentGenerator
from src.image_handler import ImageHandler

class TestErrorScenarios:
    @pytest.mark.asyncio
    async def test_content_generation_retry(self, content_generator):
        with pytest.raises(Exception):
            await content_generator.generate_article(
                topic="",  # Invalid empty topic
                keywords={}
            )
    
    @pytest.mark.asyncio
    async def test_image_handling_fallback(self, image_handler):
        result = await image_handler.fetch_images(
            topic="nonexistent_topic_123456789",
            count=1
        )
        assert result is not None  # Should return default/fallback image