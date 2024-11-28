#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 03:26:50 2024

@author: thesaint
"""

# src/advanced_quality_validator.py
from typing import Dict, List
import spacy
import textstat
from collections import defaultdict

class AdvancedQualityValidator:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.min_paragraph_words = 50
        self.max_paragraph_words = 300
        
    def validate_content_quality(self, content: str) -> Dict:
        doc = self.nlp(content)
        return {
            'readability_metrics': self._analyze_readability(content),
            'content_structure': self._analyze_structure(doc),
            'language_quality': self._analyze_language(doc),
            'seo_compliance': self._check_seo_compliance(doc)
        }
        
    def _analyze_readability(self, content: str) -> Dict:
        return {
            'flesch_reading_ease': textstat.flesch_reading_ease(content),
            'smog_index': textstat.smog_index(content),
            'dale_chall_score': textstat.dale_chall_readability_score(content),
            'avg_sentence_length': textstat.avg_sentence_length(content)
        }
        
    def _analyze_structure(self, doc) -> Dict:
        paragraphs = [p.text for p in doc.sents if len(p.text.split()) > 3]
        return {
            'paragraph_distribution': {
                'too_short': sum(1 for p in paragraphs if len(p.split()) < self.min_paragraph_words),
                'optimal': sum(1 for p in paragraphs if self.min_paragraph_words <= len(p.split()) <= self.max_paragraph_words),
                'too_long': sum(1 for p in paragraphs if len(p.split()) > self.max_paragraph_words)
            },
            'transition_words': self._count_transition_words(doc)
        }