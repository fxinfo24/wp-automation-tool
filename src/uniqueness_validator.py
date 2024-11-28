#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 01:34:10 2024

@author: thesaint
"""

# src/uniqueness_validator.py
from pathlib import Path
import hashlib
from difflib import SequenceMatcher
import logging
from datetime import datetime
from typing import Dict, List
import json
import asyncio

class UniquenessValidator:
    def __init__(self, cache_dir: str = 'data/content_cache'):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.similarity_threshold = 0.8
        self.max_retries = 3
        self.setup_logging()
        
    def setup_logging(self):
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        logging.basicConfig(
            filename=log_dir / f'uniqueness_validator_{datetime.now():%Y%m%d}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    async def check_uniqueness(self, content: str) -> Dict:
        retries = 0
        while retries < self.max_retries:
            try:
                content_hash = self._generate_hash(content)
                similarity_scores = await self._check_similarity(content)
                plagiarism_check = await self._check_plagiarism(content)
                
                result = {
                    'is_unique': max(similarity_scores.values(), default=0) < self.similarity_threshold,
                    'similarity_scores': similarity_scores,
                    'content_hash': content_hash,
                    'plagiarism_check': plagiarism_check,
                    'timestamp': datetime.now().isoformat()
                }
                
                await self._cache_content(content, content_hash, result)
                logging.info(f"Uniqueness check completed: {result['is_unique']}")
                
                return result
                
            except Exception as e:
                retries += 1
                if retries == self.max_retries:
                    logging.error(f"Uniqueness check failed after {self.max_retries} attempts: {str(e)}")
                    raise
                await asyncio.sleep(2 ** retries)
        
    def _generate_hash(self, content: str) -> str:
        return hashlib.sha256(content.encode()).hexdigest()
        
    async def _check_similarity(self, content: str) -> Dict[str, float]:
        try:
            similarity_scores = {}
            content_words = set(content.lower().split())
            
            for cached_file in self.cache_dir.glob('*.txt'):
                with open(cached_file, 'r', encoding='utf-8') as f:
                    cached_content = f.read()
                    cached_words = set(cached_content.lower().split())
                    
                    # Word-based similarity
                    word_similarity = len(content_words.intersection(cached_words)) / len(content_words.union(cached_words))
                    
                    # Sequence-based similarity
                    sequence_similarity = SequenceMatcher(None, content, cached_content).ratio()
                    
                    # Combined score
                    similarity_scores[cached_file.stem] = (word_similarity + sequence_similarity) / 2
                    
            return similarity_scores
            
        except Exception as e:
            logging.error(f"Similarity check failed: {str(e)}")
            raise
            
    async def _check_plagiarism(self, content: str) -> Dict:
        words = content.lower().split()
        word_count = len(words)
        unique_words = len(set(words))
        
        # Calculate n-gram similarity
        trigrams = set([' '.join(words[i:i+3]) for i in range(len(words)-2)])
        
        return {
            'uniqueness_ratio': unique_words / word_count if word_count > 0 else 0,
            'word_count': word_count,
            'unique_words': unique_words,
            'trigram_count': len(trigrams),
            'complexity_score': len(trigrams) / word_count if word_count > 0 else 0
        }
        
    async def _cache_content(self, content: str, content_hash: str, result: Dict) -> None:
        for attempt in range(self.max_retries):
            try:
                content_file = self.cache_dir / f'{content_hash}.txt'
                with open(content_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                result_file = self.cache_dir / f'{content_hash}_analysis.json'
                with open(result_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=4)
                    
                logging.info(f"Content cached successfully: {content_hash}")
                break
                
            except Exception as e:
                if attempt == self.max_retries - 1:
                    logging.error(f"Content caching failed after {self.max_retries} attempts: {str(e)}")
                    raise
                await asyncio.sleep(2 ** attempt)
                
    async def cleanup_old_cache(self, max_age_days: int = 30):
        try:
            current_time = datetime.now()
            for cache_file in self.cache_dir.glob('*.*'):
                file_age = datetime.fromtimestamp(cache_file.stat().st_mtime)
                if (current_time - file_age).days > max_age_days:
                    cache_file.unlink()
                    logging.info(f"Removed old cache file: {cache_file}")
        except Exception as e:
            logging.error(f"Cache cleanup failed: {str(e)}")