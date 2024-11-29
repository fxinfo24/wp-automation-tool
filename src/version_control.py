#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 02:57:12 2024

@author: thesaint
"""

# src/version_control.py

from pathlib import Path
import json
from datetime import datetime
import logging

class VersionControl:
    def __init__(self, version_dir: str = 'version_control'):
        self.version_dir = Path(version_dir)
        self.version_dir.mkdir(exist_ok=True)
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            filename=f'logs/version_control_{datetime.now():%Y%m%d}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def save_version(self, post_id: str, content: dict, version: str) -> None:
        """Save a version of content to version control"""
        try:
            version_file = self.version_dir / f"{post_id}_{version}.json"
            content['version'] = version
            content['timestamp'] = datetime.now().isoformat()
            
            with open(version_file, "w") as f:
                json.dump(content, f, indent=4)
            
            logging.info(f"Saved version {version} for post {post_id}")
        except Exception as e:
            logging.error(f"Failed to save version: {str(e)}")
            raise
    
    def get_version(self, post_id: str, version: str) -> dict:
        """Retrieve a specific version of content"""
        try:
            version_file = self.version_dir / f"{post_id}_{version}.json"
            with open(version_file, "r") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Failed to retrieve version: {str(e)}")
            raise