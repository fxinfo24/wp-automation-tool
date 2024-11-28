#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 03:19:06 2024

@author: thesaint
"""

# src/enhanced_content_generator.py
from src.seo_optimizer import SEOOptimizer
from src.content_quality import ContentQualityChecker
from src.content_generator import ContentGenerator

class EnhancedContentGenerator(ContentGenerator):
    def __init__(self, config_manager):
        super().__init__(config_manager)
        self.seo_optimizer = SEOOptimizer()
        self.quality_checker = ContentQualityChecker()
        
    async def generate_enhanced_content(self, topic: str, keywords: List[str], 
                                      word_count: int = 3200) -> Dict:
        content = await self.generate_content(topic, keywords, word_count)
        
        optimized_content = self.seo_optimizer.optimize_content(
            content, 
            keywords
        )
        
        quality_metrics = self.quality_checker.analyze_content(optimized_content)
        
        if quality_metrics['readability_score'] < 60:
            content = await self.regenerate_content(topic, keywords, word_count)
            
        return {
            'content': optimized_content,
            'metrics': quality_metrics,
            'keyword_density': self.seo_optimizer.keyword_density
        }