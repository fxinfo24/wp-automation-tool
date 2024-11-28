#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 03:22:13 2024

@author: thesaint
"""

# src/content_quality_manager.py
from typing import Dict, List
import nltk
from textblob import TextBlob
from readability import Readability

class ContentQualityManager:
    def __init__(self):
        self.readability = Readability()
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        
    def analyze_quality(self, content: str) -> Dict:
        return {
            'readability_scores': self._get_readability_scores(content),
            'content_metrics': self._analyze_content_metrics(content),
            'structure_analysis': self._analyze_structure(content)
        }
    
    def _get_readability_scores(self, content: str) -> Dict:
        return {
            'flesch_kincaid': self.readability.flesch_kincaid(content),
            'gunning_fog': self.readability.gunning_fog(content),
            'coleman_liau': self.readability.coleman_liau(content)
        }
    
    def _analyze_content_metrics(self, content: str) -> Dict:
        blob = TextBlob(content)
        return {
            'sentiment': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity,
            'word_count': len(content.split()),
            'unique_words': len(set(content.lower().split()))
        }