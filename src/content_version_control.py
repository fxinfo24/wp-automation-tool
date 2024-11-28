#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 04:02:41 2024

@author: thesaint
"""

# src/content_version_control.py
from datetime import datetime
import json
from pathlib import Path
import hashlib

class ContentVersionControl:
    def __init__(self):
        self.version_dir = Path('version_control/content')
        self.version_dir.mkdir(parents=True, exist_ok=True)
        
    def save_content_version(self, content: dict) -> str:
        content_hash = self._generate_hash(content)
        version_data = {
            'timestamp': datetime.now().isoformat(),
            'content': content,
            'hash': content_hash,
            'version': self._get_next_version(content_hash)
        }
        
        self._save_to_file(content_hash, version_data)
        return content_hash
        
    def _generate_hash(self, content: dict) -> str:
        content_str = json.dumps(content, sort_keys=True)
        return hashlib.sha256(content_str.encode()).hexdigest()[:12]
        
    def _get_next_version(self, content_hash: str) -> str:
        existing_versions = list(self.version_dir.glob(f'{content_hash}_*.json'))
        return f"1.{len(existing_versions)}.0"