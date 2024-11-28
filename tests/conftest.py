#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 01:00:21 2024

@author: thesaint
"""

# tests/conftest.py
import pytest
from unittest.mock import Mock

@pytest.fixture
def config_manager():
    mock_config = Mock()
    mock_config.get_credentials.return_value = {
        'openai': {
            'api_key': 'test_key',
            'model': 'gpt-4',
            'temperature': 0.9
        },
        'wordpress': {
            'url': 'test_url',
            'username': 'test_user',
            'password': 'test_pass'
        },
        'unsplash': {
            'access_key': 'test_key'
        }
    }
    return mock_config