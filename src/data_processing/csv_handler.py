#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 23:43:12 2024

@author: thesaint
"""

# src/data_processing/csv_handler.py
from typing import Dict, List
import pandas as pd
from pathlib import Path
import logging
from datetime import datetime

class CSVHandler:
    def __init__(self):
        self.input_dir = Path('data/input')
        self.output_dir = Path('data/output')
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            filename=f'logs/csv_handler_{datetime.now():%Y%m%d}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    async def process_batch_file(self, file_path: str) -> List[Dict]:
        try:
            df = self._read_file(file_path)
            self._validate_batch_structure(df)
            return self._prepare_batch_data(df)
        except Exception as e:
            logging.error(f"Batch file processing failed: {str(e)}")
            raise
            
    def _read_file(self, file_path: str) -> pd.DataFrame:
        file_ext = Path(file_path).suffix.lower()
        if file_ext == '.csv':
            return pd.read_csv(file_path)
        elif file_ext in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        raise ValueError(f"Unsupported file format: {file_ext}")
        
# Add to src/data_processing/csv_handler.py

    def _validate_batch_structure(self, df: pd.DataFrame) -> None:
        required_columns = [
            'topic',
            'primary_keywords',
            'additional_keywords',
            'target_audience',
            'tone',
            'word_count',
            'gpt_version'
        ]
        
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
            
        # Validate data types
        if 'word_count' in df.columns:
            invalid_counts = df[df['word_count'] < 3200]['word_count'].unique()
            if len(invalid_counts) > 0:
                raise ValueError(f"Word count must be at least 3200. Found: {invalid_counts}")
                
        # Validate GPT version
        valid_versions = ['3.5', '4', '4.0']
        if 'gpt_version' in df.columns:
            invalid_versions = df[~df['gpt_version'].isin(valid_versions)]['gpt_version'].unique()
            if len(invalid_versions) > 0:
                raise ValueError(f"Invalid GPT versions found: {invalid_versions}")

    def _prepare_batch_data(self, df: pd.DataFrame) -> List[Dict]:
        processed_data = []
        for idx, row in df.iterrows():
            try:
                processed_row = {
                    'topic': self._sanitize_text(row['topic']),
                    'primary_keywords': self._parse_keywords(row['primary_keywords']),
                    'additional_keywords': self._parse_keywords(row['additional_keywords']),
                    'target_audience': self._sanitize_text(row['target_audience']),
                    'tone': self._sanitize_text(row['tone']),
                    'word_count': int(row['word_count']),
                    'gpt_version': row['gpt_version']
                }
                processed_data.append(processed_row)
                logging.info(f"Successfully processed row {idx + 1}: {row['topic']}")
            except Exception as e:
                logging.error(f"Failed to process row {idx + 1}: {str(e)}")
                continue
        return processed_data

    def _sanitize_text(self, text: str) -> str:
        if pd.isna(text) or not str(text).strip():
            raise ValueError("Text field cannot be empty")
        return str(text).strip()

    def _parse_keywords(self, keywords_str: str) -> List[str]:
        if pd.isna(keywords_str):
            return []
        keywords = [k.strip() for k in str(keywords_str).split(',') if k.strip()]
        if not keywords:
            raise ValueError("At least one keyword must be provided")
        return keywords