#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 02:25:12 2024

@author: thesaint
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 02:25:12 2024

@author: thesaint
"""

#!/usr/bin/env python3
import asyncio
import logging
import sys
from pathlib import Path
from datetime import datetime
import argparse
from typing import Dict, List

from src.config_manager import ConfigManager
from src.content_generator import EnhancedContentGenerator
from src.image_handler import ImageHandler
from src.wordpress_poster import WordPressPoster
from src.seo_enhancer import SEOEnhancer
from src.content_validator import ContentValidator
from src.uniqueness_validator import UniquenessValidator
from src.advanced_quality_validator import AdvancedQualityValidator
from src.performance_monitor import PerformanceMonitor

MAX_RETRIES = 3
SLEEP_INTERVAL = 840  # 14 minutes in seconds

class WordPressAutomationSystem:
    def __init__(self):
        try:
            self.config = ConfigManager()
            self.content_generator = EnhancedContentGenerator(self.config)
            self.image_handler = ImageHandler(self.config)
            self.wordpress_poster = WordPressPoster(self.config)
            self.seo_enhancer = SEOEnhancer()
            self.content_validator = ContentValidator()
            self.uniqueness_validator = UniquenessValidator()
            self.quality_validator = AdvancedQualityValidator()
            self.performance_monitor = PerformanceMonitor()
            self.setup_logging()
        except Exception as e:
            logging.error(f"Initialization failed: {str(e)}")
            sys.exit("Failed to initialize automation system")
        
    def setup_logging(self):
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        logging.basicConfig(
            filename=log_dir / f'automation_{datetime.now():%Y%m%d}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    async def process_content(self, topic_data: dict):
        retries = 0
        while retries < MAX_RETRIES:
            try:
                async with asyncio.timeout(300):  # 5 minutes timeout
                    content_result = await self.content_generator.generate_enhanced_content(
                        topic_data['topic'],
                        topic_data['primary_keywords'],
                        topic_data.get('word_count', 3200),
                        gpt_version=topic_data.get('gpt_version', '4'),
                        custom_outline=topic_data.get('custom_outline')
                    )
                    
                    quality_check = await self.quality_validator.validate_content_quality(
                        content_result['content']
                    )
                    
                    if not self._meets_quality_standards(quality_check):
                        logging.warning(f"Content quality below threshold: {topic_data['topic']}")
                        return None
                    
                    images = await self._process_media_with_retry(topic_data)
                    
                    seo_result = self.seo_enhancer.optimize_content(
                        content_result['content'],
                        topic_data['primary_keywords']
                    )
                    
                    post_id = await self.wordpress_poster.create_post(
                        title=topic_data['topic'],
                        content=seo_result['optimized_content'],
                        images=images,
                        metadata={
                            'seo_metrics': seo_result['seo_metrics'],
                            'quality_metrics': quality_check
                        }
                    )
                    
                    return {
                        'post_id': post_id,
                        'metrics': {
                            'seo': seo_result['seo_metrics'],
                            'quality': quality_check,
                            'uniqueness': await self.uniqueness_validator.check_uniqueness(
                                seo_result['optimized_content']
                            )
                        }
                    }
                    
            except asyncio.TimeoutError:
                logging.error(f"Content processing timeout: {topic_data['topic']}")
                retries += 1
            except Exception as e:
                logging.error(f"Content processing failed: {str(e)}")
                retries += 1
                if retries == MAX_RETRIES:
                    logging.error(f"Max retries ({MAX_RETRIES}) reached. Skipping topic.")
                    return None
                await asyncio.sleep(2 ** retries)  # Exponential backoff

    def _meets_quality_standards(self, quality_check: dict) -> bool:
        return (
            quality_check['readability_metrics']['flesch_reading_ease'] > 60 and
            quality_check['content_structure']['paragraph_distribution']['optimal'] > 0.7
        )

    async def _process_media_with_retry(self, topic_data: Dict, max_retries: int = 3) -> List[Dict]:
        for attempt in range(max_retries):
            try:
                return await self.image_handler.fetch_and_optimize_images(
                    topic_data['topic'],
                    count=3
                )
            except Exception as e:
                if attempt == max_retries - 1:
                    logging.error(f"Media processing failed after {max_retries} attempts")
                    return []
                logging.warning(f"Media processing attempt {attempt + 1} failed: {str(e)}")
                await asyncio.sleep(2 ** attempt)

async def main():
    parser = argparse.ArgumentParser(description='WordPress Automation Tool')
    parser.add_argument('--input', required=True, help='Path to input CSV/Excel file')
    parser.add_argument('--config', default='config/config.ini', help='Path to config file')
    args = parser.parse_args()

    try:
        system = WordPressAutomationSystem()
        
        while True:
            topics = system.config.get_next_batch(args.input)
            if not topics:
                logging.info("No more topics to process")
                break
                
            for topic in topics:
                try:
                    result = await system.process_content(topic)
                    if result:
                        logging.info(f"Successfully processed: {topic['topic']}")
                    try:
                        await asyncio.sleep(SLEEP_INTERVAL)
                    except asyncio.CancelledError:
                        logging.info("Processing interrupted, shutting down gracefully...")
                        return
                except Exception as e:
                    logging.error(f"Topic processing failed: {str(e)}")
                    continue
                    
    except KeyboardInterrupt:
        logging.info("Process interrupted by user, shutting down gracefully...")
    except Exception as e:
        logging.error(f"Fatal error encountered: {str(e)}")
        sys.exit("Exiting due to fatal error")
    finally:
        logging.info("Cleaning up resources...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Script terminated by user")
        sys.exit(0)