#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 22:12:09 2024

@author: thesaint
"""

# src/input_processor.py
import pandas as pd
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class InputProcessor:
    def __init__(self, config_manager):
        self.config = config_manager
        self.required_columns = [
            'topic',
            'primary_keywords',
            'additional_keywords',
            'target_audience',
            'tone',
            'word_count',
            'gpt_version',
            'custom_outline'
        ]
        self.valid_gpt_versions = ['3.5', '4', '4.0']
        self.min_word_count = 3200
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            filename=f'logs/input_processor_{datetime.now():%Y%m%d}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    async def process_input_file(self, file_path: str) -> List[Dict]:
        try:
            df = self._read_input_file(file_path)
            self._validate_columns(df)
            self._validate_data_types(df)
            processed_data = self._process_rows(df)
            logging.info(f"Successfully processed {len(processed_data)} rows from {file_path}")
            return processed_data
        except Exception as e:
            logging.error(f"Input processing failed: {str(e)}")
            raise

    def _read_input_file(self, file_path: str) -> pd.DataFrame:
        file_ext = Path(file_path).suffix.lower()
        if file_ext == '.csv':
            return pd.read_csv(file_path)
        elif file_ext in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        raise ValueError(f"Unsupported file format: {file_ext}")

    def _validate_columns(self, df: pd.DataFrame) -> None:
        missing_columns = set(self.required_columns) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

    def _validate_data_types(self, df: pd.DataFrame) -> None:
        # GPT version validation
        if 'gpt_version' in df.columns:
            invalid_versions = df[~df['gpt_version'].isin(self.valid_gpt_versions)]['gpt_version'].unique()
            if len(invalid_versions) > 0:
                raise ValueError(f"Invalid GPT versions found: {invalid_versions}")
        
        # Word count validation
        if 'word_count' in df.columns:
            invalid_counts = df[df['word_count'] < self.min_word_count]['word_count'].unique()
            if len(invalid_counts) > 0:
                raise ValueError(f"Word count must be at least {self.min_word_count}. Found: {invalid_counts}")
        
        # Target audience validation
        if 'target_audience' in df.columns:
            if df['target_audience'].isnull().any():
                raise ValueError("Target audience cannot be empty")

    def _process_rows(self, df: pd.DataFrame) -> List[Dict]:
        processed_data = []
        for idx, row in df.iterrows():
            try:
                processed_row = {
                    'topic': self._validate_text(row['topic'], 'Topic'),
                    'primary_keywords': self._parse_keywords(row['primary_keywords']),
                    'additional_keywords': self._parse_keywords(row['additional_keywords']),
                    'target_audience': self._validate_text(row['target_audience'], 'Target audience'),
                    'tone': self._validate_text(row['tone'], 'Tone'),
                    'word_count': int(row['word_count']),
                    'gpt_version': row['gpt_version'],
                    'custom_outline': self._parse_outline(row.get('custom_outline', ''))
                }
                processed_data.append(processed_row)
                logging.info(f"Successfully processed row {idx + 1}: {row['topic']}")
            except Exception as e:
                logging.error(f"Failed to process row {idx + 1}: {str(e)}")
                raise

        return processed_data

    def _validate_text(self, text: str, field_name: str) -> str:
        if pd.isna(text) or not str(text).strip():
            raise ValueError(f"{field_name} cannot be empty")
        return str(text).strip()

    def _parse_keywords(self, keywords_str: str) -> List[str]:
        if pd.isna(keywords_str):
            return []
        keywords = [k.strip() for k in str(keywords_str).split(',') if k.strip()]
        if not keywords:
            raise ValueError("At least one keyword must be provided")
        return keywords

    def _parse_outline(self, outline_str: str) -> Optional[List[str]]:
        if pd.isna(outline_str):
            return None
        outline = [line.strip() for line in str(outline_str).split('\n') if line.strip()]
        return outline if outline else None