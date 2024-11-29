# tests/unit/test_image_handler.py

#!/usr/bin/env python3
import pytest
from unittest.mock import patch, Mock
from src.image_handler import ImageHandler

class TestImageHandler:
    @pytest.fixture
    async def image_handler(self, config_manager):
        return ImageHandler(config_manager)

    @pytest.mark.asyncio
    async def test_fetch_images(self, image_handler):
        with patch('requests.get') as mock_get:
            mock_get.return_value.content = b"fake_image_data"
            mock_get.return_value.headers = {'content-type': 'image/jpeg'}
            
            images = await image_handler.fetch_and_optimize_images(
                topic="Test Topic",
                count=3
            )
            assert len(images) == 3
            assert all('url' in img for img in images)

    @pytest.mark.asyncio
    async def test_image_optimization(self, image_handler):
        test_image = b"fake_image_data"
        with patch('PIL.Image.open') as mock_open:
            mock_image = Mock()
            mock_image.size = (2000, 1500)
            mock_open.return_value = mock_image
            
            optimized = await image_handler._optimize_image(test_image)
            assert optimized is not None

    @pytest.mark.asyncio
    async def test_error_handling(self, image_handler):
        with patch('requests.get', side_effect=Exception("API Error")):
            with pytest.raises(Exception):
                await image_handler.fetch_and_optimize_images("Test", 1)