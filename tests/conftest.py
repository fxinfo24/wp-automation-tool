#!/usr/bin/env python3


# tests/conftest.py

import pytest
import asyncio
from unittest.mock import Mock, patch
from pathlib import Path

@pytest.fixture(scope="function")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

@pytest.fixture
def config_manager():
    mock_config = Mock()
    def get_credentials(service=None):
        credentials = {
            'openai': {
                'api_key': 'sk-test-key',
                'model': 'gpt-4',
                'temperature': 0.9,
                'max_tokens': 4000,
                'timeout': 30
            },
            'wordpress': {
                'url': 'https://test.com/xmlrpc.php',
                'username': 'test_user',
                'password': 'test_pass',
                'timeout': 30
            },
            'unsplash': {
                'access_key': 'test-key',
                'timeout': 30
            },
            'youtube': {
                'api_key': 'test-key',
                'timeout': 30
            }
        }
        return credentials[service] if service else credentials
    mock_config.get_credentials = get_credentials
    return mock_config

@pytest.fixture
def mock_openai_client():
    with patch('openai.OpenAI') as mock:
        mock.return_value.chat.completions.create.return_value.choices = [
            Mock(message=Mock(content="Test content"))
        ]
        yield mock

@pytest.fixture
def mock_wordpress_client():
    with patch('wordpress_xmlrpc.Client') as mock:
        mock.return_value.call.return_value = 123
        yield mock

@pytest.fixture
def mock_unsplash_client():
    with patch('requests.get') as mock:
        mock.return_value.status_code = 200
        mock.return_value.content = b"test_image_data"
        mock.return_value.headers = {'content-type': 'image/jpeg'}
        yield mock

@pytest.fixture
def test_topic_data():
    return {
        'topic': 'Test Topic',
        'primary_keywords': ['test', 'keywords'],
        'additional_keywords': ['more', 'keywords'],
        'target_audience': 'testers',
        'tone': 'professional',
        'word_count': 3200,
        'gpt_version': '4'
    }

@pytest.fixture
def test_data_dir(tmp_path):
    """Create temporary test data directory."""
    data_dir = tmp_path / "test_data"
    data_dir.mkdir()
    return data_dir

@pytest.fixture
def version_control_dir(tmp_path):
    """Create temporary directory for version control testing."""
    vc_dir = tmp_path / "version_control"
    vc_dir.mkdir()
    return vc_dir