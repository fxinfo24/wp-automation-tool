#!/usr/bin/env python3

# tests/performance/test_performance.py
#!/usr/bin/env python3
import pytest
import time
import asyncio
from unittest.mock import patch, Mock
from src.automation_manager import AutomationManager

class TestPerformanceMetrics:
    @pytest.fixture
    async def automation_manager(self, config_manager):
        # Ensure config_manager returns proper credentials
        config_manager.get_credentials.return_value = {
            'openai': {
                'api_key': 'test-key',
                'model': 'gpt-4',
                'temperature': 0.9,
                'max_tokens': 4000
            },
            'wordpress': {
                'url': 'http://test.com/xmlrpc.php',
                'username': 'test_user',
                'password': 'test_pass'
            },
            'unsplash': {
                'access_key': 'test-key'
            }
        }
        return AutomationManager(config_manager)

    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_content_generation_speed(self, automation_manager):
        start_time = time.time()
        test_data = {
            'topic': 'Performance Test',
            'primary_keywords': ['performance test'],
            'additional_keywords': ['speed test'],
            'target_audience': 'testers',
            'tone': 'technical',
            'word_count': 3200
        }
        
        with patch('openai.OpenAI') as mock_openai:
            mock_openai.return_value.chat.completions.create.return_value.choices = [
                Mock(message=Mock(content="Test content"))
            ]
            content = await automation_manager.content_generator.generate_article(
                test_data['topic'],
                test_data
            )
            generation_time = time.time() - start_time
            assert generation_time < 60
            assert isinstance(content, str)

    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_posting_interval(self, automation_manager):
        test_topics = [
            {
                'topic': f'Performance Test {i}',
                'primary_keywords': ['test'],
                'additional_keywords': ['performance'],
                'target_audience': 'developers',
                'tone': 'technical',
                'word_count': 3200
            } for i in range(2)
        ]
        
        with patch('openai.OpenAI') as mock_openai:
            mock_openai.return_value.chat.completions.create.return_value.choices = [
                Mock(message=Mock(content="Test content"))
            ]
            with patch('src.wordpress_poster.WordPressPoster.create_post', return_value=123):
                start_time = time.time()
                await automation_manager.process_batch(test_topics)
                total_time = time.time() - start_time
                assert total_time >= 840  # 14 minutes interval