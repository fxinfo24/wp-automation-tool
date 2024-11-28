#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 02:24:52 2024

@author: thesaint
"""

# tests/test_rate_limiter.py
import pytest
import time
from src.rate_limiter import RateLimiter

def test_rate_limiter():
    limiter = RateLimiter()
    
    @limiter.limit_rate('test', 2)
    def test_function():
        return time.time()
    
    first_call = test_function()
    second_call = test_function()
    
    assert second_call - first_call >= 2

# tests/test_version_control.py
import pytest
from src.version_control import VersionControl
import json

@pytest.fixture
def version_control():
    return VersionControl()

def test_version_saving(version_control, tmp_path):
    content = {"title": "Test", "body": "Content"}
    version_control.version_dir = tmp_path
    version_control.save_version("test123", content, "1.0")
    
    saved_file = tmp_path / "test123_v1.0.json"
    assert saved_file.exists()
    
    with open(saved_file) as f:
        saved_content = json.load(f)
        assert saved_content['content'] == content