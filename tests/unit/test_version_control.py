# tests/unit/test_version_control.py
#!/usr/bin/env python3
import pytest
from pathlib import Path
import json
from datetime import datetime
from unittest.mock import patch
from src.version_control import VersionControl

class TestVersionControl:
    @pytest.fixture
    def version_control(self, tmp_path):
        """Create a temporary version control instance for testing."""
        vc = VersionControl(version_dir=str(tmp_path))
        return vc

    @pytest.mark.unit
    def test_save_version(self, version_control, tmp_path):
        test_content = {
            "title": "Test Article",
            "content": "Test content",
            "timestamp": datetime.now().isoformat()
        }
        post_id = "test123"
        version = "1.0.0"
        
        version_control.save_version(post_id, test_content, version)
        
        version_file = tmp_path / f"{post_id}_{version}.json"
        assert version_file.exists()
        
        with open(version_file, 'r', encoding='utf-8') as f:
            saved_content = json.load(f)
            assert saved_content['title'] == test_content['title']
            assert saved_content['version'] == version
            assert 'timestamp' in saved_content

    @pytest.mark.unit
    def test_get_version(self, version_control, tmp_path):
        test_content = {
            "title": "Test Article",
            "content": "Test content",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat()
        }
        post_id = "test456"
        version = "1.0.0"
        
        version_file = tmp_path / f"{post_id}_{version}.json"
        with open(version_file, 'w', encoding='utf-8') as f:
            json.dump(test_content, f)
            
        retrieved_content = version_control.get_version(post_id, version)
        assert retrieved_content['title'] == test_content['title']
        assert retrieved_content['version'] == version

    @pytest.mark.unit
    def test_version_not_found(self, version_control):
        with pytest.raises(FileNotFoundError) as exc_info:
            version_control.get_version("nonexistent", "1.0.0")
        assert "Version file not found" in str(exc_info.value)

    @pytest.mark.unit
    def test_version_format_validation(self, version_control):
        test_content = {"title": "Test"}
        
        # Valid version formats
        valid_versions = ["1.0.0", "2.1.0", "0.0.1"]
        for version in valid_versions:
            version_control.save_version("test", test_content, version)
        
        # Invalid version formats
        invalid_versions = ["1.0", "1", "1.0.0.0", "invalid"]
        for version in invalid_versions:
            with pytest.raises(ValueError) as exc_info:
                version_control.save_version("test", test_content, version)
            assert "Invalid version format" in str(exc_info.value)

    @pytest.mark.unit
    def test_version_history(self, version_control, tmp_path):
        post_id = "test789"
        versions = ["1.0.0", "1.0.1", "1.0.2"]
        
        for version in versions:
            content = {
                "title": f"Test Article {version}",
                "content": f"Content version {version}",
                "timestamp": datetime.now().isoformat()
            }
            version_control.save_version(post_id, content, version)
        
        history = version_control.get_version_history(post_id)
        assert len(history) == len(versions)
        assert all(v in [h['version'] for h in history] for v in versions)

    @pytest.mark.unit
    def test_cleanup_old_versions(self, version_control, tmp_path):
        post_id = "test_cleanup"
        versions = [f"1.0.{i}" for i in range(5)]
        
        # Create test versions
        for version in versions:
            content = {
                "title": f"Test {version}",
                "content": "Test content",
                "timestamp": datetime.now().isoformat()
            }
            version_control.save_version(post_id, content, version)
        
        # Keep only latest 3 versions
        version_control.cleanup_old_versions(max_versions=3)
        remaining_files = list(tmp_path.glob("*.json"))
        assert len(remaining_files) == 3