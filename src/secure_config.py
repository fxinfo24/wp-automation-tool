#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 03:49:04 2024

@author: thesaint
"""

# src/secure_config.py
from cryptography.fernet import Fernet
import configparser
import os
from pathlib import Path

class SecureConfigManager:
    def __init__(self):
        self.key_file = Path('config/.key')
        self.config_file = Path('config/config.ini')
        self._initialize_encryption()
        
    def _initialize_encryption(self):
        if not self.key_file.exists():
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
        self.cipher_suite = Fernet(self.key_file.read_bytes())
        
    def encrypt_value(self, value: str) -> str:
        return self.cipher_suite.encrypt(value.encode()).decode()
        
    def decrypt_value(self, encrypted_value: str) -> str:
        return self.cipher_suite.decrypt(encrypted_value.encode()).decode()
        
    def save_credentials(self, section: str, credentials: dict):
        config = configparser.ConfigParser()
        if self.config_file.exists():
            config.read(self.config_file)
            
        if section not in config:
            config[section] = {}
            
        for key, value in credentials.items():
            config[section][key] = self.encrypt_value(value)
            
        with open(self.config_file, 'w') as f:
            config.write(f)