#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 06:50:05 2024

@author: thesaint
"""

# src/content_generator.py

from openai import OpenAI
from typing import Dict, List
import logging
from datetime import datetime
from pathlib import Path
import asyncio

class EnhancedContentGenerator:
    def __init__(self, config_manager):
        self.config = config_manager.get_credentials('openai')
        self.client = OpenAI(api_key=self.config['api_key'])
        self.temperature = 0.9
        self.max_tokens = int(self.config.get('max_tokens', 4000))
        self.max_retries = 3
        self.setup_logging()
        
    def setup_logging(self):
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        logging.basicConfig(
            filename=log_dir / f'content_generator_{datetime.now():%Y%m%d}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    async def generate_enhanced_content(
        self, 
        topic: str, 
        primary_keywords: List[str],
        word_count: int = 3200,
        gpt_version: str = '4',
        custom_outline: str = None
    ) -> Dict:
        try:
            keywords = {
                'primary': primary_keywords,
                'secondary': [],
                'audience': 'general',
                'tone': 'professional'
            }
            
            content = await self._generate_with_retry(topic, keywords)
            
            if custom_outline:
                content = await self.modify_outline(content, custom_outline.split('\n'))
                
            validation = await self.validate_content(content, keywords)
            
            return {
                'content': content,
                'word_count': len(content.split()),
                'validation': validation,
                'keywords_used': self._count_keywords(content, primary_keywords)
            }
        except Exception as e:
            logging.error(f"Enhanced content generation failed: {str(e)}")
            raise

    async def _generate_with_retry(self, topic: str, keywords: Dict) -> str:
        retries = 0
        while retries < self.max_retries:
            try:
                return await self.generate_article(topic, keywords)
            except Exception as e:
                retries += 1
                if retries == self.max_retries:
                    logging.error(f"Max retries ({self.max_retries}) reached. Error: {str(e)}")
                    raise
                logging.warning(f"Attempt {retries} failed: {str(e)}")
                await asyncio.sleep(2 ** retries)  # Exponential backoff
            
    async def generate_article(self, topic: str, keywords: Dict) -> str:
        try:
            prompt = self._create_prompt(topic, keywords)
            response = await self.client.chat.completions.create(
                model=self.config['model'],
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Content generation failed: {str(e)}")
            raise
            
    def _create_prompt(self, topic: str, keywords: Dict) -> str:
        return f"""Write a unique, original article on: {topic}
                Primary keywords: {keywords['primary']}
                Additional keywords: {keywords.get('secondary', [])}
                Target audience: {keywords.get('audience', 'general')}
                Tone: {keywords.get('tone', 'professional')}
                Length: 3200 words
                Structure:
                1. Creative Hook & Title
                   - Start with compelling SEO-optimized title
                   - Use 8-10 word hook
                   - Create engaging introduction
                
                2. Body Sections with H2, H3, H4 headings
                   - Use logical heading hierarchy
                   - Include bullet points and lists
                   - Add formatting for emphasis
                
                3. Engaging Extras
                   - Add FAQs section
                   - Include examples and case studies
                   - Reference credible sources
                
                4. Bonus Tip & Call to Benefit
                   - Provide actionable bonus tip
                   - End with engagement prompt
                
                Temperature: {self.temperature}"""
                
    async def modify_outline(self, content: str, new_outline: List[str]) -> str:
        try:
            outline_prompt = self._create_outline_prompt(content, new_outline)
            response = await self.client.chat.completions.create(
                model=self.config['model'],
                messages=[{"role": "user", "content": outline_prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Outline modification failed: {str(e)}")
            raise
            
    def _create_outline_prompt(self, content: str, new_outline: List[str]) -> str:
        return f"""Restructure this article according to the following outline while maintaining the original content and SEO optimization:

                Original content: {content}
                New outline:
                {self._format_outline(new_outline)}
                
                Maintain all SEO keywords and optimize headings."""
                
    def _format_outline(self, outline: List[str]) -> str:
        return "\n".join([f"- {item}" for item in outline])
        
    async def validate_content(self, content: str, keywords: Dict) -> Dict:
        word_count = len(content.split())
        keyword_count = sum(content.lower().count(kw.lower()) for kw in keywords['primary'])
        
        return {
            'word_count': word_count >= 3200,
            'keyword_density': keyword_count >= 20,
            'structure': all(heading in content for heading in ['<h1>', '<h2>', '<h3>']),
            'has_faq': '<faq>' in content.lower(),
            'metrics': {
                'total_words': word_count,
                'keyword_occurrences': keyword_count
            }
        }
        
    def _count_keywords(self, content: str, keywords: List[str]) -> Dict[str, int]:
        content_lower = content.lower()
        return {
            keyword: content_lower.count(keyword.lower())
            for keyword in keywords
        }