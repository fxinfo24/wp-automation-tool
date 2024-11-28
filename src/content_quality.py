#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 20:59:50 2024

@author: thesaint
"""

# src/content_quality.py
from typing import Dict, List
import re
import nltk
from textblob import TextBlob
import logging
from datetime import datetime

class ContentQualityAnalyzer:
    def __init__(self):
        self.min_word_count = 3200
        self.ideal_keyword_density = 0.02
        self.setup_logging()
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
        
    def setup_logging(self):
        logging.basicConfig(
            filename=f'logs/content_quality_{datetime.now():%Y%m%d}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    async def analyze_content(self, content: str, keywords: List[str]) -> Dict:
        try:
            return {
                'readability_metrics': self._analyze_readability(content),
                'keyword_optimization': self._analyze_keywords(content, keywords),
                'content_structure': self._analyze_structure(content),
                'quality_score': self._calculate_quality_score(content),
                'engagement_metrics': self._analyze_engagement(content),
                'seo_score': self._calculate_seo_score(content, keywords)
            }
        except Exception as e:
            logging.error(f"Content quality analysis failed: {str(e)}")
            raise
            
    def _analyze_readability(self, content: str) -> Dict:
        blob = TextBlob(content)
        sentences = blob.sentences
        
        return {
            'avg_sentence_length': sum(len(str(s).split()) for s in sentences) / len(sentences),
            'paragraph_count': len(content.split('\n\n')),
            'readability_score': self._calculate_flesch_score(content)
        }
        
    def _analyze_keywords(self, content: str, keywords: List[str]) -> Dict:
        keyword_density = {}
        words = content.lower().split()
        
        for keyword in keywords:
            count = len(re.findall(rf'\b{keyword.lower()}\b', content.lower()))
            density = count / len(words)
            keyword_density[keyword] = {
                'count': count,
                'density': density,
                'in_headings': self._check_keyword_in_headings(content, keyword)
            }
            
        return keyword_density
        
    def _analyze_engagement(self, content: str) -> Dict:
        return {
            'question_count': len(re.findall(r'\?', content)),
            'call_to_actions': len(re.findall(r'!|(?i)click|subscribe|comment|share', content)),
            'subheading_count': len(re.findall(r'<h[2-4]', content)),
            'internal_links': len(re.findall(r'<a\s+href=[^>]+>', content))
        }
        
    def _calculate_seo_score(self, content: str, keywords: List[str]) -> float:
        scores = {
            'keyword_presence': self._check_keyword_presence(content, keywords),
            'heading_optimization': self._check_heading_optimization(content, keywords),
            'content_length': len(content.split()) >= self.min_word_count,
            'readability': self._calculate_flesch_score(content) > 60
        }
        return sum(scores.values()) / len(scores) * 100
        
    def _check_keyword_presence(self, content: str, keywords: List[str]) -> bool:
        content_lower = content.lower()
        return all(
            len(re.findall(rf'\b{keyword.lower()}\b', content_lower)) >= 20 
            for keyword in keywords
        )
        
    def _check_heading_optimization(self, content: str, keywords: List[str]) -> bool:
        headings = re.findall(r'<h[1-4]>(.*?)</h[1-4]>', content, re.IGNORECASE)
        keywords_lower = [k.lower() for k in keywords]
        return any(
            any(keyword in heading.lower() for keyword in keywords_lower)
            for heading in headings
        )
        
    def _calculate_flesch_score(self, content: str) -> float:
        sentences = nltk.sent_tokenize(content)
        words = content.split()
        
        total_words = len(words)
        total_sentences = len(sentences)
        total_syllables = sum(self._count_syllables(word) for word in words)
        
        if total_sentences == 0 or total_words == 0:
            return 0.0
            
        return 206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (total_syllables / total_words)
        
    def _count_syllables(self, word: str) -> int:
        word = word.lower()
        count = 0
        vowels = "aeiouy"
        previous_char_is_vowel = False
        
        if word.endswith('e'):
            word = word[:-1]
            
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_char_is_vowel:
                count += 1
            previous_char_is_vowel = is_vowel
            
        if count == 0:
            count = 1
        return count
        
    def _calculate_quality_score(self, content: str) -> float:
        metrics = {
            'readability': self._calculate_flesch_score(content) > 60,
            'length': len(content.split()) >= self.min_word_count,
            'structure': bool(re.search(r'<h[1-4]>', content)),
            'paragraphs': len(content.split('\n\n')) >= 5
        }
        return sum(metrics.values()) / len(metrics) * 100
        
    def _check_keyword_in_headings(self, content: str, keyword: str) -> bool:
        headings = re.findall(r'<h[1-4]>(.*?)</h[1-4]>', content, re.IGNORECASE)
        return any(keyword.lower() in heading.lower() for heading in headings)
        
    def _analyze_structure(self, content: str) -> Dict:
        return {
            'heading_count': len(re.findall(r'<h[1-4]>', content)),
            'paragraph_count': len(content.split('\n\n')),
            'list_items': len(re.findall(r'<li>', content)),
            'image_count': len(re.findall(r'<img', content))
        }