#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 03:27:31 2024

@author: thesaint
"""

# src/seo_quality_checker.py
from typing import Dict, List, Tuple
import re
from urllib.parse import urlparse

class SEOQualityChecker:
    def __init__(self):
        self.heading_hierarchy = ['h1', 'h2', 'h3']
        self.optimal_keyword_density = (0.01, 0.03)
        
    def check_seo_quality(self, content: str, keywords: List[str]) -> Dict:
        return {
            'keyword_optimization': self._analyze_keyword_optimization(content, keywords),
            'heading_structure': self._validate_heading_structure(content),
            'link_quality': self._analyze_links(content),
            'meta_optimization': self._check_meta_tags(content)
        }
        
    def _analyze_keyword_optimization(self, content: str, keywords: List[str]) -> Dict:
        word_count = len(content.split())
        keyword_positions = self._get_keyword_positions(content, keywords)
        
        return {
            'density': {kw: len(pos)/word_count for kw, pos in keyword_positions.items()},
            'first_paragraph': any(pos < 100 for positions in keyword_positions.values() for pos in positions),
            'in_headings': self._check_keywords_in_headings(content, keywords),
            'distribution_score': self._calculate_distribution_score(keyword_positions, word_count)
        }
        
    def _validate_heading_structure(self, content: str) -> Dict:
        headings = self._extract_headings(content)
        return {
            'hierarchy_valid': self._check_heading_hierarchy(headings),
            'keyword_presence': self._check_heading_keywords(headings),
            'length_distribution': self._analyze_heading_lengths(headings)
        }