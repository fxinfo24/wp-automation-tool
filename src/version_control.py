#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 02:57:12 2024

@author: thesaint
"""

# src/version_control.py
from datetime import datetime
import json

class VersionControl:
    def __init__(self):
        self.version = "1.0.0"
        self.version_history = []
        
    def increment_version(self, version_type='patch'):
        major, minor, patch = map(int, self.version.split('.'))
        if version_type == 'major':
            major += 1
            minor = patch = 0
        elif version_type == 'minor':
            minor += 1
            patch = 0
        else:
            patch += 1
        self.version = f"{major}.{minor}.{patch}"
        
    def log_change(self, change_type, description):
        change = {
            'version': self.version,
            'timestamp': datetime.now().isoformat(),
            'type': change_type,
            'description': description
        }
        self.version_history.append(change)
        self._save_history()
        
    def _save_history(self):
        with open('version_control/history.json', 'w') as f:
            json.dump(self.version_history, f, indent=4)