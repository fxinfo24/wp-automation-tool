#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 03:49:57 2024

@author: thesaint
"""

# src/logging_manager.py
import logging
import logging.handlers
from datetime import datetime
from pathlib import Path

class LoggingManager:
    def __init__(self):
        self.log_dir = Path('logs')
        self.log_dir.mkdir(exist_ok=True)
        self._setup_logging()
        
    def _setup_logging(self):
        log_file = self.log_dir / f'wordpress_automation_{datetime.now():%Y%m%d}.log'
        formatter = logging.Formatter(
            '%(asctime)s - %(version)s - %(levelname)s - %(message)s'
        )
        
        # Size-based rotation (1MB)
        size_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=1024 * 1024,  # 1MB
            backupCount=5
        )
        size_handler.setFormatter(formatter)
        
        # Time-based rotation (2 minutes)
        time_handler = logging.handlers.TimedRotatingFileHandler(
            log_file.with_suffix('.timed.log'),
            when='M',
            interval=2,  # 2 minutes
            backupCount=5
        )
        time_handler.setFormatter(formatter)
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # Root logger configuration
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(size_handler)
        logger.addHandler(time_handler)
        logger.addHandler(console_handler)