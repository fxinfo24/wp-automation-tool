#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 02:11:17 2024

@author: thesaint
"""

# tests/test_automation_manager.py
import pytest
from unittest.mock import Mock, patch
from src.automation_manager import AutomationManager

@pytest.fixture
def mock_dependencies():
    return {
        'config_manager': Mock(),
        'content_generator': Mock(),
        'image_handler': Mock(),
        'wordpress_poster': Mock()
    }

@pytest.fixture
def automation_manager(mock_dependencies):
    return AutomationManager(**mock_dependencies)

def test_process_single_post(automation_manager):
    test_data = {
        'topic': 'Test Topic',
        'keywords': 'test, keywords',
        'title': 'Test Title'
    }
    
    automation_manager.content_generator.generate_content.return_value = 'Test Content'
    automation_manager.image_handler.fetch_images.return_value = ['test.jpg']
    automation_manager.wordpress_poster.create_post.return_value = '123'
    
    post_id = automation_manager.process_single_post(test_data)
    
    assert post_id == '123'
    automation_manager.content_generator.generate_content.assert_called_once()
    automation_manager.image_handler.fetch_images.assert_called_once()
    automation_manager.wordpress_poster.create_post.assert_called_once()