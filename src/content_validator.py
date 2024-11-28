#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 20:12:30 2024

@author: thesaint
"""

# src/content_validator.py
from typing import Dict, List
import re
import logging

class ContentValidator:
    def __init__(self):
        self.required_elements = {
            'headings': r'<h[1-4].*?>.*?</h[1-4]>',
            'paragraphs': r'<p>.*?</p>',
            'images': r'<img.*?>',
            'links': r'<a.*?href=.*?>.*?</a>'
        }
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            filename='logs/content_validator.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    async def validate_content(self, content: str, requirements: Dict) -> Dict:
        try:
            validation_results = {
                'meets_word_count': self._check_word_count(content, requirements.get('min_words', 3200)),
                'has_required_elements': self._check_required_elements(content),
                'keyword_presence': self._check_keyword_presence(content, requirements.get('keywords', [])),
                'structure_validation': self._validate_structure(content)
            }
            
            validation_results['is_valid'] = all(validation_results.values())
            return validation_results
            
        except Exception as e:
            logging.error(f"Content validation failed: {str(e)}")
            raise