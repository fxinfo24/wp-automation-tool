# WordPress Automation Tool

## Overview
An advanced Python automation tool for creating and publishing high-quality content to WordPress websites using OpenAI GPT, Unsplash images, and YouTube integration. This tool generates SEO-optimized articles with rich media content while maintaining posting intervals of 14 minutes.

## Features

### Content Generation
- AI-powered article writing using OpenAI GPT (versions 3.5, 4, 4.0)
- Customizable word count (default: 3200 words)
- SEO optimization with keyword integration
- Custom outline support
- Plagiarism-free content generation
- Temperature control for creativity (0.9)

### Media Integration
- Automatic image selection from Unsplash
- Image optimization and resizing
- YouTube video embedding
- Featured image selection
- Media library integration

### WordPress Integration
- Direct posting via XML-RPC
- Category and tag management
- Post scheduling
- Bulk content processing

### Data Management
- CSV/Excel input support
- Content caching
- Version control
- Detailed logging

## Installation Guide

### Prerequisites
- Python 3.12
- VS Code with Python extensions
- WordPress website with XML-RPC enabled
- Required API keys:
  - OpenAI API key
  - Unsplash access key
  - YouTube API key
  - WordPress credentials

### Project Structure Setup
```bash
# Create main project directory
mkdir wordpress_automation_tool
cd wordpress_automation_tool

# Create source directories
mkdir -p src/{data_processing,media_system,content_management,quality_assurance}
mkdir -p src/quality_assurance/{unit_tests,integration_tests,performance_tests,documentation}

# Create other directories
mkdir -p tests config data/{input,output,cache} logs docs

# Create Python package files
touch src/__init__.py
touch src/data_processing/__init__.py
touch src/media_system/__init__.py
touch src/content_management/__init__.py
touch src/quality_assurance/__init__.py

# Create component files
touch src/data_processing/{csv_handler,input_validator,keyword_manager,config_validator}.py
touch src/media_system/{youtube_integration,image_optimizer,media_library,featured_image}.py
touch src/content_management/{post_scheduler,bulk_processor,queue_manager,status_tracker}.py

# Create configuration files
touch config/{config.ini,config.example.ini}
touch {main.py,requirements.txt,README.md,.gitignore,pytest.ini}
```

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

### Input Data Format (data/topics.csv)
```csv
topic,primary_keywords,additional_keywords,target_audience,tone,word_count,gpt_version,custom_outline,category,tags
"Benefits of Organic Gardening","organic gardening tips","sustainable farming,composting,natural fertilizers","eco-conscious beginners","friendly",3200,4,"Introduction\nBasics\nTips\nConclusion","Gardening","organic,sustainability"
```

### Configuration File (config/config.ini)
```ini
[openai]
api_key = your_openai_key
model = gpt-4
temperature = 0.9
max_tokens = 4000

[wordpress]
url = https://your-wordpress-site.com/xmlrpc.php
username = your_username
password = your_app_password

[unsplash]
access_key = your_unsplash_key

[youtube]
api_key = your_youtube_api_key

[rate_limits]
openai_requests_per_minute = 20
unsplash_requests_per_hour = 50
wordpress_requests_per_minute = 30

[general]
post_interval = 14
word_count = 3200
default_language = en
image_count = 3

[media]
image_max_width = 1200
image_max_height = 800
image_quality = 85
featured_image_required = true
```

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test categories
pytest tests/unit_tests/
pytest tests/integration_tests/
pytest tests/performance_tests/
```

### Performance Monitoring
```bash
# Generate performance report
python -m src.performance_monitor --report
```

## Usage
```bash
# Basic usage
python main.py --input data/topics.csv

# With custom config
python main.py --input data/topics.csv --config config/custom_config.ini
```

## Error Handling
- Check logs/ directory for detailed error messages
- Automatic retries for API failures
- Rate limiting protection
- Media fallback options

## Security Notes
- Never commit API keys
- Use .gitignore for sensitive files
- Encrypt credentials in config.ini
- Regular security audits

## Contributing
1. Fork the repository
2. Create a feature branch
3. Follow PEP 8 style guide
4. Add tests for new features
5. Submit pull request

To deploy new versions of the WordPress Automation Tool, follow these steps:

## Deployment Process

1. **Environment Validation**
```bash
python deploy.py --check-environment
```
This validates your deployment environment including WordPress credentials, API keys, and required permissions.

2. **Version Management**
The script automatically:
- Increments the patch version (e.g., 1.0.0 to 1.0.1)
- Logs deployment changes
- Updates version history

3. **Production Deployment**
```bash
python deploy.py --environment production
```

4. **Staging Deployment**
```bash
python deploy.py --environment staging
```

## Deployment Checklist

Before deploying:
- Ensure all tests pass (`pytest`)
- Verify API credentials in config.ini
- Check rate limits configuration
- Validate WordPress XML-RPC access
- Confirm media storage permissions

## Post-Deployment Verification
- Monitor logs for any errors
- Verify WordPress connectivity
- Test content generation
- Check media upload functionality
- Confirm posting intervals (14 minutes)

- The deployment script manages these processes automatically while maintaining version control and logging all changes for tracking purposes[1].

### Performance Monitoring
```bash
# Check performance metrics
python -m src.performance_monitor

# Generate performance report
python -m src.performance_monitor --report
```

### Debugging
- Set DEBUG=True in config.ini for detailed logging
- Check logs/ directory for detailed error messages
- Use VS Code's debugging features with provided launch.json

### Best Practices
1. Always run tests before committing
2. Follow PEP 8 style guide
3. Update requirements.txt when adding dependencies
4. Keep API keys secure and never commit them
5. Document code changes in CHANGELOG.md

### Common Issues
1. Rate Limiting
```python
# Adjust rate limits in config.ini
[rate_limits]
openai_requests_per_minute = 20
unsplash_requests_per_hour = 50
wordpress_requests_per_minute = 30
```

2. Memory Usage
```bash
# Monitor memory usage
python -m memory_profiler main.py
```

3. Error Recovery
- Check error logs in logs/
- Implement automatic retries
- Use backup APIs when available

### These additions provide comprehensive testing instructions and development guidelines for contributors and users

To deploy new versions of the WordPress Automation Tool, follow these steps:

## Deployment Process

1. **Environment Validation**
```bash
python deploy.py --check-environment
```
This validates your deployment environment including WordPress credentials, API keys, and required permissions.

2. **Version Management**
The script automatically:
- Increments the patch version (e.g., 1.0.0 to 1.0.1)
- Logs deployment changes
- Updates version history

3. **Production Deployment**
```bash
python deploy.py --environment production
```

4. **Staging Deployment**
```bash
python deploy.py --environment staging
```

## Deployment Checklist

Before deploying:
- Ensure all tests pass (`pytest`)
- Verify API credentials in config.ini
- Check rate limits configuration
- Validate WordPress XML-RPC access
- Confirm media storage permissions

## Post-Deployment Verification
- Monitor logs for any errors
- Verify WordPress connectivity
- Test content generation
- Check media upload functionality
- Confirm posting intervals (14 minutes)

The deployment script manages these processes automatically while maintaining version control and logging all changes for tracking purposes[1].

## License
MIT License - see LICENSE file for details

