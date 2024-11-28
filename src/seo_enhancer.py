#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 03:22:53 2024

@author: thesaint
"""

# src/seo_enhancer.py
from typing import Dict, List
import re
from collections import Counter

class SEOEnhancer:
    def __init__(self):
        self.heading_patterns = {
            'h1': r'<h1.*?>(.*?)</h1>',
            'h2': r'<h2.*?>(.*?)</h2>',
            'h3': r'<h3.*?>(.*?)</h3>'
        }
    
    def optimize_content(self, content: str, keywords: List[str], 
                        target_density: float = 0.02) -> Dict:
        optimized = self._optimize_headings(content, keywords)
        optimized = self._optimize_meta_tags(optimized, keywords)
        optimized = self._optimize_keyword_placement(optimized, keywords)
        
        return {
            'optimized_content': optimized,
            'seo_metrics': self._calculate_seo_metrics(optimized, keywords)
        }
    
    def _optimize_keyword_placement(self, content: str, keywords: List[str]) -> str:
        paragraphs = content.split('\n\n')
        optimized_paragraphs = []
        
        for i, para in enumerate(paragraphs):
            if i == 0 or i == len(paragraphs) - 1:
                # Ensure keywords in first and last paragraphs
                para = self._insert_keywords(para, keywords[:2])
            optimized_paragraphs.append(para)
            
        return '\n\n'.join(optimized_paragraphs)
    
    def _calculate_seo_metrics(self, content: str, keywords: List[str]) -> Dict:
        return {
            'keyword_density': self._calculate_keyword_density(content, keywords),
            'heading_optimization': self._analyze_headings(content, keywords),
            'meta_tags_present': bool(re.search(r'<meta.*?>', content)),
            'internal_links': len(re.findall(r'<a.*?href=.*?>', content))
        }