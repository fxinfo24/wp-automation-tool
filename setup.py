#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 03:16:03 2024

@author: thesaint
"""

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
    url="https://github.com/yourusername/wordpress-automation-tool",
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
        "openai>=1.0.0",
        "python-wordpress-xmlrpc>=2.3",
        "Pillow>=10.0.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.1",
        "python-unsplash>=1.1.0",
        "google-api-python-client>=2.0.0",
        "pandas>=2.1.0",
        "numpy>=1.24.0",
        "pytest>=7.4.0",
        "pytest-cov>=4.1.0",
        "pytest-asyncio>=0.21.0",
        "responses>=0.23.0",
        "cryptography>=41.0.0",
        "python-jose>=3.3.0",
        "structlog>=23.1.0",
        "python-json-logger>=2.0.7",
        "black>=23.9.1",
        "flake8>=6.1.0",
        "mypy>=1.5.1",
        "gitpython>=3.1.40",
        "aiohttp>=3.8.5",
        "asyncio>=3.4.3"
    ],
    entry_points={
        "console_scripts": [
            "wp-automation=main:main",
        ],
    },
    package_data={
        "wordpress_automation_tool": [
            "config/*.ini",
            "data/topics.csv",
        ],
    },
    include_package_data=True,
    zip_safe=False
)