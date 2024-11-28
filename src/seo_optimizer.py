#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 18:25:45 2024

@author: thesaint
"""

# src/seo_optimizer.py
from typing import Dict, List
import re
from textblob import TextBlob

class SEOOptimizer:
    def __init__(self):
        self.keyword_density_target = (0.02, 0.03)  # 2-3% density
        
    def optimize_content(self, content: str, keywords: Dict) -> Dict:
        optimized_content = content
        optimized_content = self._optimize_title(optimized_content, keywords['primary'])
        optimized_content = self._optimize_headings(optimized_content, keywords)
        optimized_content = self._optimize_keyword_placement(optimized_content, keywords)
        
        return {
            'content': optimized_content,
            'meta_data': self._generate_meta_data(optimized_content, keywords),
            'metrics': self._calculate_seo_metrics(optimized_content, keywords)
        }
        
    def _optimize_title(self, content: str, primary_keyword: str) -> str:
        title_match = re.search(r'<h1>(.*?)</h1>', content)
        if title_match:
            title = title_match.group(1)
            if primary_keyword.lower() not in title.lower():
                title = f"{title} - {primary_keyword}"
            return content.replace(title_match.group(0), f"<h1>{title}</h1>")
        return content
        
    def _optimize_headings(self, content: str, keywords: Dict) -> str:
        for level in range(2, 5):  # H2 to H4
            pattern = rf'<h{level}>(.*?)</h{level}>'
            headings = re.finditer(pattern, content)
            for heading in headings:
                optimized_heading = self._inject_keywords(
                    heading.group(1),
                    keywords['primary'],
                    keywords['secondary']
                )
                content = content.replace(heading.group(0), f"<h{level}>{optimized_heading}</h{level}>")
        return content
        
    def _generate_meta_data(self, content: str, keywords: Dict) -> Dict:
        blob = TextBlob(content)
        return {
            'title': f"{keywords['primary']} - {' '.join(content.split()[:8])}",
            'description': f"{' '.join(blob.sentences[0].words[:30])}... Learn more about {keywords['primary']}",
            'keywords': ', '.join(keywords['primary'] + keywords['secondary'])
        }