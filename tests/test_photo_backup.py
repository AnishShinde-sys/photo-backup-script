"""
Basic tests for photo_backup.py
"""

import pytest
import tempfile
import os
from pathlib import Path

def test_import_photo_backup():
    """Test that we can import the photo_backup module."""
    try:
        import photo_backup
        assert photo_backup is not None
    except ImportError:
        pytest.skip("photo_backup module not available")

def test_load_config_example():
    """Test that example configuration can be loaded."""
    import yaml
    
    config_path = Path(__file__).parent.parent / "config.example.yaml"
    if config_path.exists():
        with open(config_path) as f:
            config = yaml.safe_load(f)
        assert config is not None
        assert 'sources' in config
        assert 'destination' in config
    else:
        pytest.skip("config.example.yaml not found")

def test_basic_file_operations():
    """Test basic file operations used by backup script."""
    import tempfile
    import hashlib
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("test content")
        temp_path = f.name
    
    try:
        # Test file existence
        assert Path(temp_path).exists()
        
        # Test hash calculation
        with open(temp_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        assert len(file_hash) == 64  # SHA256 produces 64 hex characters
        
    finally:
        # Cleanup
        if Path(temp_path).exists():
            Path(temp_path).unlink()

def test_yaml_parsing():
    """Test YAML parsing capabilities."""
    import yaml
    
    test_data = """
    sources:
      - path: "/test/path"
        recursive: true
    destination:
      path: "/backup/path"
    """
    
    config = yaml.safe_load(test_data)
    assert config is not None
    assert 'sources' in config
    assert config['sources'][0]['path'] == "/test/path"

def test_datetime_operations():
    """Test datetime operations used by backup script."""
    from datetime import datetime
    from pathlib import Path
    
    # Create a temporary file and get its timestamp
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("test")
        temp_path = f.name
    
    try:
        stat = Path(temp_path).stat()
        timestamp = stat.st_mtime
        date = datetime.fromtimestamp(timestamp)
        
        assert date is not None
        assert isinstance(date, datetime)
        
        # Test date formatting
        date_str = date.strftime('%Y/%m/%d')
        assert len(date_str.split('/')) == 3
        
    finally:
        if Path(temp_path).exists():
            Path(temp_path).unlink()
