#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 02:54:41 2024

@author: thesaint
"""

# src/deployment_manager.py
import yaml
import os
from pathlib import Path

class DeploymentManager:
    def __init__(self):
        self.config_path = Path('config/deployment.yml')
        self.environment = os.getenv('ENVIRONMENT', 'staging')
        
    def load_config(self):
        with open(self.config_path) as f:
            config = yaml.safe_load(f)
            return config['environment'][self.environment]
            
    def validate_environment(self):
        config = self.load_config()
        required_keys = ['host', 'wordpress_url', 'api_rate_limits']
        return all(key in config for key in required_keys)