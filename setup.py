#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 07:16:03 2024

@author: thesaint
"""
# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wordpress_automation_tool",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for automated WordPress content creation and posting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fxinfo24/wp-automation-tool",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    install_requires=[
        # Content Generation
        "openai>=1.0.0",
        "python-wordpress-xmlrpc>=2.3",
        
        # Media Handling
        "Pillow>=10.0.0",
        "python-unsplash>=1.1.0",
        "google-api-python-client>=2.0.0",
        
        # Data Processing
        "pandas>=2.1.0",
        "numpy>=1.24.0",
        
        # Testing
        "pytest>=7.4.0",
        "pytest-cov>=6.0.0",
        "pytest-asyncio>=0.24.0",
        "pytest-mock>=3.14.0",
        "coverage>=7.4.0",
        "responses>=0.23.0",
        "pytest-timeout>=2.1.0",
        
        # Security and Configuration
        "python-dotenv>=1.0.0",
        "cryptography>=41.0.0",
        "python-jose>=3.3.0",
        "pyjwt>=2.8.0",
        
        # Logging and Monitoring
        "structlog>=23.1.0",
        "python-json-logger>=2.0.7",
        "rich>=13.7.0",
        
        # Development Tools
        "black>=23.9.1",
        "flake8>=6.1.0",
        "mypy>=1.5.1",
        "isort>=5.13.0",
        
        # Version Control
        "gitpython>=3.1.40",
        
        # HTTP and Async
        "aiohttp>=3.8.5",
        "asyncio>=3.4.3",
        "requests>=2.31.0",
        "httpx>=0.25.0",
        
        # Configuration
        "pyyaml>=6.0.1",
        "python-decouple>=3.8.0"
    ],
    entry_points={
        "console_scripts": [
            "wp-automation=main:main",
        ],
    },
    package_data={
        "wordpress_automation_tool": [
            "config/*.ini",
            "config/*.example.ini",
            "data/topics.csv",
            "data/content_cache/*",
            "data/image_cache/*",
            "data/post_history/*",
            "data/media/*",
            "logs/*",
            "version_control/*",
            "tests/fixtures/*"
        ],
    },
    include_package_data=True,
    zip_safe=False,
    test_suite="tests",
    python_requires=">=3.12"
)