#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 04:03:24 2024

@author: thesaint
"""

# tests/test_critical_path.py
import pytest
from src.content_generator import ContentGenerator
from src.wordpress_poster import WordPressPoster
from src.image_handler import ImageHandler

class TestCriticalPath:
    @pytest.fixture
    def test_content(self):
        return {
            'topic': 'Organic Gardening',
            'keywords': ['organic gardening tips', 'sustainable farming'],
            'word_count': 3200
        }
    
    def test_content_generation_flow(self, content_generator, test_content):
        content = content_generator.generate_content(
            topic=test_content['topic'],
            keywords=test_content['keywords'],
            word_count=test_content['word_count']
        )
        
        assert len(content.split()) >= test_content['word_count']
        assert all(kw.lower() in content.lower() for kw in test_content['keywords'])
        
    def test_image_handling_flow(self, image_handler, test_content):
        images = image_handler.fetch_images(test_content['topic'])
        assert len(images) >= 2
        
        optimized_images = [
            image_handler.optimize_image(img) 
            for img in images
        ]
        assert all(img.size[0] <= 800 for img in optimized_images)