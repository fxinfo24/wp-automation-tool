#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 03:32:16 2024

@author: thesaint
"""

# src/config_manager.py
import configparser
import logging
from pathlib import Path
from typing import Dict, List
from cryptography.fernet import Fernet
from datetime import datetime
import pandas as pd

class ConfigManager:
    def __init__(self):
        self.config_dir = Path('config')
        self.config_file = self.config_dir / 'config.ini'
        self.key_file = self.config_dir / '.key'
        self.setup_logging()
        self._initialize_encryption()
        self._load_config()
        
    def setup_logging(self):
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        logging.basicConfig(
            filename=log_dir / f'config_manager_{datetime.now():%Y%m%d}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def _initialize_encryption(self):
        try:
            if not self.key_file.exists():
                key = Fernet.generate_key()
                with open(self.key_file, 'wb') as f:
                    f.write(key)
            with open(self.key_file, 'rb') as f:
                self.cipher_suite = Fernet(f.read())
            logging.info("Encryption initialized successfully")
        except Exception as e:
            logging.error(f"Encryption initialization failed: {str(e)}")
            raise
            
    def _load_config(self):
        try:
            self.config = configparser.ConfigParser()
            if self.config_file.exists():
                self.config.read(self.config_file)
                self._validate_and_update_config()
            else:
                self._create_default_config()
        except Exception as e:
            logging.error(f"Config loading failed: {str(e)}")
            raise
            
    def _create_default_config(self):
        self.config['openai'] = {
            'api_key': '',
            'model': 'gpt-4',
            'temperature': '0.9',
            'max_tokens': '4000'
        }
        self.config['wordpress'] = {
            'url': '',
            'username': '',
            'password': ''
        }
        self.config['unsplash'] = {
            'access_key': ''
        }
        self.config['youtube'] = {
            'api_key': ''
        }
        self.config['rate_limits'] = {
            'openai_requests_per_minute': '20',
            'unsplash_requests_per_hour': '50',
            'wordpress_requests_per_minute': '30'
        }
        self.config['general'] = {
            'post_interval': '14',
            'word_count': '3200'
        }
        self.save_config()
        
    def get_credentials(self, service: str) -> Dict:
        try:
            if service not in self.config:
                raise ValueError(f"Service {service} not found in config")
                
            credentials = dict(self.config[service])
            for key in credentials:
                if any(secret in key for secret in ['password', 'api_key', 'access_key']):
                    try:
                        credentials[key] = self._decrypt_value(credentials[key])
                    except:
                        credentials[key] = self._encrypt_and_store_value(service, key, credentials[key])
            return credentials
            
        except Exception as e:
            logging.error(f"Failed to get credentials for {service}: {str(e)}")
            raise
            
    def get_next_batch(self, input_file: str = None) -> List[Dict]:
        try:
            if not input_file:
                return []
                
            input_path = Path(input_file)
            if not input_path.exists():
                logging.error(f"Input file not found: {input_file}")
                return []
                
            if input_path.suffix.lower() == '.csv':
                df = pd.read_csv(input_path)
            elif input_path.suffix.lower() in ['.xlsx', '.xls']:
                df = pd.read_excel(input_path)
            else:
                logging.error(f"Unsupported file format: {input_path.suffix}")
                return []
                
            self._validate_batch_data(df)
            return df.to_dict('records')
            
        except Exception as e:
            logging.error(f"Failed to read batch file: {str(e)}")
            return []
            
    def _validate_batch_data(self, df: pd.DataFrame) -> None:
        required_columns = [
            'topic', 'primary_keywords', 'additional_keywords',
            'target_audience', 'tone', 'word_count', 'gpt_version'
        ]
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
            
    def _validate_and_update_config(self):
        required_sections = [
            'openai', 'wordpress', 'unsplash', 'youtube',
            'rate_limits', 'general'
        ]
        for section in required_sections:
            if section not in self.config:
                self._create_default_config()
                break
                
    def _encrypt_value(self, value: str) -> str:
        return self.cipher_suite.encrypt(value.encode()).decode()
        
    def _decrypt_value(self, encrypted_value: str) -> str:
        return self.cipher_suite.decrypt(encrypted_value.encode()).decode()
        
    def _encrypt_and_store_value(self, service: str, key: str, value: str) -> str:
        encrypted_value = self._encrypt_value(value)
        self.config[service][key] = encrypted_value
        self.save_config()
        return value
        
    def save_config(self):
        try:
            with open(self.config_file, 'w') as f:
                self.config.write(f)
            logging.info("Configuration saved successfully")
        except Exception as e:
            logging.error(f"Failed to save config: {str(e)}")
            raise