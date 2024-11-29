#!/usr/bin/env python3

# tests/unit/test_content_generator.py
import pytest
from unittest.mock import patch
from src.content_generator import EnhancedContentGenerator

class TestContentGenerator:
    @pytest.fixture
    async def content_generator(self, config_manager):
        return EnhancedContentGenerator(config_manager)

    @pytest.mark.asyncio
    async def test_generate_article(self, content_generator):
        test_data = {
            'topic': 'Test Topic',
            'primary_keywords': ['test keyword'],
            'additional_keywords': ['more keywords'],
            'target_audience': 'testers',
            'tone': 'technical'
        }
        
        with patch('openai.OpenAI') as mock_openai:
            mock_openai.return_value.chat.completions.create.return_value.choices[0].message.content = "Test content"
            content = await content_generator.generate_article(test_data['topic'], test_data)
            assert len(content) > 0
            assert isinstance(content, str)

    @pytest.mark.asyncio
    async def test_content_validation(self, content_generator):
        test_content = "Test content" * 1000
        validation = await content_generator.validate_content(
            test_content,
            {'primary': ['test']}
        )
        assert 'word_count' in validation
        assert 'keyword_density' in validation

    @pytest.mark.asyncio
    async def test_outline_modification(self, content_generator):
        original_content = "Original content"
        new_outline = ["Introduction", "Section 1", "Conclusion"]
        
        with patch('openai.OpenAI') as mock_openai:
            mock_openai.return_value.chat.completions.create.return_value.choices[0].message.content = "Modified content"
            modified = await content_generator.modify_outline(original_content, new_outline)
            assert modified != original_content