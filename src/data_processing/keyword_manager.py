#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 01:38:33 2024

@author: thesaint
"""

# src/data_processing/keyword_manager.py
from typing import Dict, List
import logging
from datetime import datetime
from collections import defaultdict
import re

class KeywordManager:
    def __init__(self):
        self.keyword_stats = defaultdict(int)
        self.min_keyword_count = 20
        self.max_keyword_count = 30
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            filename=f'logs/keyword_manager_{datetime.now():%Y%m%d}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    async def process_keywords(self, topic: str, keywords: Dict) -> Dict:
        try:
            primary_keywords = self._validate_primary_keywords(keywords['primary'])
            secondary_keywords = self._validate_secondary_keywords(keywords['secondary'])
            
            return {
                'primary': primary_keywords,
                'secondary': secondary_keywords,
                'density_targets': self._calculate_density_targets(primary_keywords, secondary_keywords),
                'heading_keywords': self._select_heading_keywords(primary_keywords),
                'seo_analysis': self._analyze_seo_potential(primary_keywords, secondary_keywords)
            }
        except Exception as e:
            logging.error(f"Keyword processing failed for topic {topic}: {str(e)}")
            raise
            
    def _validate_primary_keywords(self, keywords: List[str]) -> List[str]:
        if not keywords:
            raise ValueError("Primary keywords cannot be empty")
        validated = [k.strip().lower() for k in keywords if k.strip()]
        if not validated:
            raise ValueError("No valid primary keywords after validation")
        return validated
        
    def _validate_secondary_keywords(self, keywords: List[str]) -> List[str]:
        return [k.strip().lower() for k in keywords if k.strip()]
        
    def _calculate_density_targets(self, primary: List[str], secondary: List[str]) -> Dict:
        total_keywords = len(primary) + len(secondary)
        return {
            'primary_per_keyword': self.min_keyword_count,
            'secondary_per_keyword': 10,
            'total_target': total_keywords * 15,
            'density_range': {
                'min': self.min_keyword_count,
                'max': self.max_keyword_count
            }
        }
        
    def _select_heading_keywords(self, primary_keywords: List[str]) -> List[str]:
        return primary_keywords[:3]  # Use top 3 primary keywords for headings
        
    def _analyze_seo_potential(self, primary: List[str], secondary: List[str]) -> Dict:
        return {
            'primary_keywords': {
                'count': len(primary),
                'recommended_usage': {kw: self.min_keyword_count for kw in primary}
            },
            'secondary_keywords': {
                'count': len(secondary),
                'recommended_usage': {kw: 10 for kw in secondary}
            },
            'total_keywords': len(primary) + len(secondary)
        }
        
    async def analyze_keyword_usage(self, content: str, keywords: Dict) -> Dict:
        try:
            return {
                'keyword_counts': self._count_keyword_occurrences(content, keywords),
                'heading_usage': self._analyze_heading_keywords(content, keywords['primary']),
                'density_analysis': self._analyze_keyword_density(content, keywords),
                'optimization_score': self._calculate_optimization_score(content, keywords)
            }
        except Exception as e:
            logging.error(f"Keyword usage analysis failed: {str(e)}")
            raise
            
    def _count_keyword_occurrences(self, content: str, keywords: Dict) -> Dict:
        content_lower = content.lower()
        counts = {}
        for keyword_type, keyword_list in keywords.items():
            counts[keyword_type] = {
                keyword: len(re.findall(rf'\b{re.escape(keyword)}\b', content_lower))
                for keyword in keyword_list
            }
        return counts
        
    def _analyze_heading_keywords(self, content: str, primary_keywords: List[str]) -> Dict:
        headings = re.findall(r'<h[1-4]>(.*?)</h[1-4]>', content, re.IGNORECASE)
        return {
            keyword: [h for h in headings if keyword.lower() in h.lower()]
            for keyword in primary_keywords
        }
        
    def _analyze_keyword_density(self, content: str, keywords: Dict) -> Dict:
        word_count = len(content.split())
        densities = {}
        for keyword_type, keyword_list in keywords.items():
            total_occurrences = sum(
                len(re.findall(rf'\b{re.escape(keyword)}\b', content.lower()))
                for keyword in keyword_list
            )
            densities[keyword_type] = (total_occurrences / word_count) * 100 if word_count > 0 else 0
        return densities
        
    def _calculate_optimization_score(self, content: str, keywords: Dict) -> float:
        counts = self._count_keyword_occurrences(content, keywords)
        heading_usage = self._analyze_heading_keywords(content, keywords['primary'])
        
        score = 0
        max_score = 100
        
        # Score based on keyword counts
        for keyword, count in counts['primary'].items():
            if self.min_keyword_count <= count <= self.max_keyword_count:
                score += 40 / len(counts['primary'])
                
        # Score based on heading usage
        for keyword, headings in heading_usage.items():
            if headings:
                score += 30 / len(heading_usage)
                
        # Score based on density
        densities = self._analyze_keyword_density(content, keywords)
        if 1.5 <= densities['primary'] <= 2.5:
            score += 30
            
        return min(score, max_score)