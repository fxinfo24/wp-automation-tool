#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 03:06:28 2024

@author: thesaint
"""

# src/error_handler.py
import logging
from functools import wraps
from typing import Callable, Any

class ErrorHandler:
    def __init__(self):
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            filename='logs/error.log',
            level=logging.ERROR,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    @staticmethod
    def handle_api_errors(retry_count: int = 3, delay: int = 5):
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                attempts = 0
                while attempts < retry_count:
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        attempts += 1
                        logging.error(f"Attempt {attempts} failed: {str(e)}")
                        if attempts == retry_count:
                            raise
            return wrapper
        return decorator