#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 02:08:44 2024

@author: thesaint
"""

# tests/test_performance.py
import pytest
import time
import asyncio
from src.automation_manager import AutomationManager

class TestPerformanceMetrics:
    @pytest.fixture
    async def automation_manager(self, config_manager):
        return AutomationManager(config_manager)
    
    @pytest.mark.performance
    async def test_content_generation_speed(self, automation_manager):
        start_time = time.time()
        test_data = {
            'topic': 'Test Performance',
            'primary_keywords': ['performance test'],
            'additional_keywords': ['speed test'],
            'target_audience': 'testers',
            'tone': 'technical',
            'word_count': 3200
        }
        
        content = await automation_manager.content_generator.generate_article(
            test_data['topic'],
            test_data
        )
        
        generation_time = time.time() - start_time
        assert generation_time < 60  # Should complete within 60 seconds
        assert len(content.split()) >= 3200
        
    @pytest.mark.performance
    async def test_batch_processing_performance(self, automation_manager):
        test_batch = [
            {
                'topic': f'Performance Test {i}',
                'primary_keywords': ['test keyword'],
                'additional_keywords': ['performance testing'],
                'target_audience': 'developers',
                'tone': 'technical',
                'word_count': 3200
            } for i in range(3)
        ]
        
        start_time = time.time()
        results = await automation_manager.process_batch(test_batch)
        total_time = time.time() - start_time
        
        assert total_time < 180  # 3 minutes for 3 posts
        assert all(r['status'] == 'published' for r in results)
        
    @pytest.mark.performance
    async def test_media_processing_speed(self, automation_manager):
        start_time = time.time()
        result = await automation_manager.image_handler.fetch_and_optimize_images(
            topic="Performance Testing",
            count=3
        )
        
        processing_time = time.time() - start_time
        assert processing_time < 30  # 30 seconds max for image processing
        assert len(result) == 3
        
    @pytest.mark.performance
    async def test_wordpress_posting_speed(self, automation_manager):
        test_content = {
            'title': 'Performance Test Post',
            'content': 'Test content' * 1000,  # Simulate real content length
            'featured_image': {'data': b'test', 'id': 'test_id'},
            'categories': ['test'],
            'tags': ['performance']
        }
        
        start_time = time.time()
        post_id = await automation_manager.wordpress_poster.create_post(test_content)
        posting_time = time.time() - start_time
        
        assert posting_time < 20  # 20 seconds max for posting
        assert post_id is not None