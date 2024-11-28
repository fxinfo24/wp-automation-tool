#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 03:53:22 2024

@author: thesaint
"""

# src/version_manager.py
from datetime import datetime
import git
import logging

class VersionManager:
    def __init__(self, repo_path='.'):
        self.repo = git.Repo(repo_path)
        self.current_version = "1.0.0"
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            filename=f'logs/version_control_{datetime.now():%Y%m%d}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def commit_changes(self, message: str) -> bool:
        try:
            self.repo.index.add('*')
            self.repo.index.commit(message)
            logging.info(f"Committed changes: {message}")
            return True
        except Exception as e:
            logging.error(f"Failed to commit changes: {str(e)}")
            return False
    
    def create_tag(self, tag_name: str, message: str) -> bool:
        try:
            self.repo.create_tag(tag_name, message=message)
            logging.info(f"Created tag: {tag_name}")
            return True
        except Exception as e:
            logging.error(f"Failed to create tag: {str(e)}")
            return False