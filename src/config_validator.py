#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 03:50:42 2024

@author: thesaint
"""

# src/config_validator.py
from typing import Dict
import jsonschema
import yaml

class ConfigValidator:
    def __init__(self):
        self.schema = self._load_schema()
        
    def _load_schema(self) -> Dict:
        return {
            "type": "object",
            "required": ["openai", "wordpress", "unsplash"],
            "properties": {
                "openai": {
                    "type": "object",
                    "required": ["api_key", "model", "temperature"],
                    "properties": {
                        "api_key": {"type": "string"},
                        "model": {"type": "string"},
                        "temperature": {"type": "number"}
                    }
                },
                "wordpress": {
                    "type": "object",
                    "required": ["url", "username", "password"],
                    "properties": {
                        "url": {"type": "string", "format": "uri"},
                        "username": {"type": "string"},
                        "password": {"type": "string"}
                    }
                }
            }
        }
        
    def validate_config(self, config: Dict) -> bool:
        try:
            jsonschema.validate(instance=config, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            logging.error(f"Configuration validation failed: {str(e)}")
            return False