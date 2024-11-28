# docs/user_guide.md
Based on the project requirements and search results, here's the enhanced README.md content. I'll restructure it to be more concise and better organized:

# WordPress Automation Tool

## Overview
An advanced Python automation tool for creating and publishing high-quality content to WordPress websites using OpenAI GPT, Unsplash images, and YouTube integration. Creates SEO-optimized articles with rich media content at 14-minute intervals.

## Core Features

### Content Generation
- AI-powered article writing (GPT-3.5, 4, 4.0)
- 3200-word default length with customization
- SEO optimization and keyword integration
- Custom outline support
- Temperature control (0.9) for creativity
- Plagiarism detection

### Media Integration
- Unsplash image selection and optimization
- YouTube video embedding
- Featured image management
- Media library integration
- Image size and quality control

### WordPress Integration
- XML-RPC posting system
- Category and tag management
- Scheduled posting
- Bulk content processing
- Media upload handling

## Quick Start

### Prerequisites
```bash
# System Requirements
Python 3.12
VS Code + Python extensions
WordPress site with XML-RPC
```

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/wordpress-automation-tool.git
cd wordpress_automation_tool

# Set up environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration
1. Copy example configuration:
```bash
cp config/config.example.ini config/config.ini
```

2. Add your API credentials:
```ini
[openai]
api_key = your_openai_key
model = gpt-4

[wordpress]
url = https://your-site.com/xmlrpc.php
username = your_username
password = your_app_password
```

### Basic Usage
```bash
# Run with default configuration
python main.py --input data/topics.csv

# Run with custom config
python main.py --input data/topics.csv --config config/custom_config.ini
```

## Input Format

### Topics CSV Structure
```csv
topic,primary_keywords,additional_keywords,target_audience,tone,word_count,gpt_version
"Topic Title","main keyword","keyword1,keyword2","audience","tone",3200,4
```

## Development

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/
```

### Deployment
```bash
# Validate environment
python deploy.py --check-environment

# Deploy to production
python deploy.py --environment production
```

### Monitoring
```bash
# Check performance
python -m src.performance_monitor --report

# Monitor memory usage
python -m memory_profiler main.py
```

## Troubleshooting

### Common Issues
- API rate limits exceeded
- WordPress XML-RPC connection failures
- Media processing errors
- Content generation timeouts

### Error Recovery
- Check logs in logs/ directory
- Verify API credentials
- Adjust rate limits in config.ini
- Enable DEBUG mode for detailed logging

## Security
- Store API keys securely
- Use .gitignore for sensitive files
- Enable WordPress security features
- Regular security audits

## Contributing
1. Fork repository
2. Create feature branch
3. Follow PEP 8
4. Add tests
5. Submit pull request

## License
MIT License - see LICENSE file

This enhanced README provides a clearer, more concise structure while maintaining all essential information for users and developers.
