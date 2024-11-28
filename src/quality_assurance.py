#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 18:21:16 2024

@author: thesaint
"""

# src/quality_assurance.py
from typing import Dict, List
import re
import nltk
from textblob import TextBlob

class ContentQualityAssurance:
    def __init__(self):
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        
    def analyze_content(self, content: str, keywords: List[str]) -> Dict:
        return {
            'readability_metrics': self._check_readability(content),
            'keyword_optimization': self._analyze_keywords(content, keywords),
            'content_structure': self._analyze_structure(content),
            'engagement_metrics': self._measure_engagement(content)
        }
        
    def _check_readability(self, content: str) -> Dict:
        sentences = nltk.sent_tokenize(content)
        words_per_sentence = len(content.split()) / len(sentences)
        
        return {
            'avg_sentence_length': words_per_sentence,
            'paragraph_count': len(content.split('\n\n')),
            'readability_score': self._calculate_readability_score(content)
        }
        
    def _analyze_keywords(self, content: str, keywords: List[str]) -> Dict:
        keyword_density = {}
        for keyword in keywords:
            count = len(re.findall(rf'\b{keyword}\b', content, re.IGNORECASE))
            density = count / len(content.split())
            keyword_density[keyword] = density
            
        return {
            'keyword_density': keyword_density,
            'keyword_in_headings': self._check_keywords_in_headings(content, keywords)
        }