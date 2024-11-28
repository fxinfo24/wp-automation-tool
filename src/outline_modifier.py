#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 20:11:53 2024

@author: thesaint
"""

# src/outline_modifier.py
from typing import Dict, List
import logging

class OutlineModifier:
    def __init__(self, content_generator):
        self.content_generator = content_generator
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            filename='logs/outline_modifier.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    async def modify_outline(self, content: str, modifications: Dict) -> str:
        try:
            sections = self._extract_sections(content)
            modified_sections = self._apply_modifications(sections, modifications)
            return self._rebuild_content(modified_sections)
        except Exception as e:
            logging.error(f"Outline modification failed: {str(e)}")
            raise
            
    def _extract_sections(self, content: str) -> List[Dict]:
        sections = []
        current_section = {'level': 0, 'title': '', 'content': ''}
        
        for line in content.split('\n'):
            if line.startswith('#'):
                if current_section['content']:
                    sections.append(current_section.copy())
                level = line.count('#')
                current_section = {
                    'level': level,
                    'title': line.strip('# '),
                    'content': ''
                }
            else:
                current_section['content'] += line + '\n'
                
        if current_section['content']:
            sections.append(current_section)
            
        return sections