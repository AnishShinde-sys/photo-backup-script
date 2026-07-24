# Photo Backup Script

Automated photo backup and synchronization tool for organizing and preserving your digital photo collection.

## Overview

The Photo Backup Script provides a reliable way to backup photos from various sources (cameras, phones, external drives) to organized storage locations with automatic deduplication, metadata preservation, and comprehensive error handling.

## Features

- **Automated Detection**: Automatically detects and backs up new photos from specified source directories
- **Intelligent Organization**: Organizes photos by date or flat structure
- **Deduplication**: Prevents duplicate files using content-based SHA256 hashing
- **Metadata Preservation**: Maintains file timestamps during copying
- **Incremental Backups**: Only processes new or modified files for efficiency
- **Cross-Platform Support**: Works on macOS, Linux, and Windows
- **Configurable**: Flexible configuration options for different backup strategies
- **Comprehensive Logging**: Detailed logs and backup statistics
- **Safety Features**: Dry-run mode, file size limits, and error handling

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone this repository:
```bash
git clone https://github.com/AnishShinde-sys/photo-backup-script.git
cd photo-backup-script
```

2. Install dependencies:
```bash
pip install -r requirements.txt
# Or for development with all testing tools:
pip install -e ".[dev]"
```

3. Configure your backup settings:
```bash
cp config.example.yaml config.yaml
# Edit config.yaml with your source and destination paths
```

### Development Installation

For development with testing and linting tools:
```bash
pip install -e ".[dev]"
```

This installs pytest, coverage tools, flake8, black, pylint, bandit, and safety.

## Usage

### Basic Backup

```bash
python photo_backup.py
```

### Command-Line Options

```bash
# Show help
python photo_backup.py --help

# Dry run to see what would be backed up
python photo_backup.py --dry-run

# Backup from specific source (overrides config)
python photo_backup.py --source /path/to/photos

# Verbose output
python photo_backup.py --verbose

# Debug mode with detailed logging
python photo_backup.py --debug

# Use custom configuration file
python photo_backup.py --config /path/to/custom-config.yaml

# Force full re-scan of source directory
python photo_backup.py --force-rescan
```

### Using as Installed Package

If installed via pip:
```bash
photo-backup --config config.yaml
photo-backup --dry-run --verbose
```

## Configuration

The script uses a YAML configuration file to define backup behavior. Here's the structure:

### Basic Configuration

```yaml
sources:
  - path: "/Users/username/Pictures/Camera"
    recursive: true
    file_types: ["jpg", "jpeg", "png", "raw", "heic", "tiff", "bmp", "gif"]

destination:
  path: "/Volumes/BackupDrive/Photos"
  organization: "date"  # options: date, flat
  date_format: "%Y/%m/%d"

options:
  deduplicate: true
  preserve_metadata: true
  verify_checksums: true
  max_file_size_mb: 100
  batch_size: 100  # Process files in batches for memory efficiency
```

### Configuration Options

**Sources:**
- `path`: Source directory path
- `recursive`: Scan subdirectories (true/false)
- `file_types`: List of file extensions to backup

**Destination:**
- `path`: Destination directory path
- `organization`: File organization strategy ("date" or "flat")
- `date_format`: Date format for folder structure (Python strftime format)

**Options:**
- `deduplicate`: Skip duplicate files based on content hash
- `preserve_metadata`: Maintain file timestamps
- `verify_checksums`: Verify file integrity after copying
- `max_file_size_mb`: Maximum file size to process
- `batch_size`: Number of files to process in each batch

## Organization Strategies

### Date-based Organization

Organizes photos by year, month, and day:

```
destination/
├── 2023/
│   ├── 01/
│   │   ├── 15/
│   │   │   ├── photo1.jpg
│   │   │   └── photo2.jpg
│   │   └── 16/
│   │   │   └── photo3.jpg
```

You can customize the date format in the configuration:
- `%Y/%m/%d` - Year/Month/Day (default)
- `%Y/%m` - Year/Month
- `%Y-%m-%d` - Year-Month-Day flat format

### Flat Structure

Places all files in the destination directory:

```
destination/
├── photo1.jpg
├── photo2.jpg
└── photo3.jpg
```

## Backup Statistics

The script provides a comprehensive summary after each backup:

```
==================================================
BACKUP SUMMARY
==================================================
Files processed: 42
Files copied: 38
Files skipped (duplicates/size): 4
Errors: 0
Total bytes saved: 125,829,120
==================================================
```

## Logging

Logs are written to `logs/photo_backup.log` and include:
- Timestamp for each operation
- File processing details
- Error messages and warnings
- Backup statistics

### Log Levels

- **INFO**: Normal operations (default)
- **DEBUG**: Detailed diagnostic information (`--debug`)
- **ERROR**: Error conditions

## Testing

The project includes comprehensive tests:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=photo_backup --cov-report=term-missing

# Run specific test
pytest tests/test_photo_backup.py::test_load_config_example
```

### Test Coverage

Current test coverage includes:
- Configuration loading and validation
- File operations and hash calculation
- YAML parsing
- DateTime operations
- Import functionality

## Development

### Code Quality Tools

The project uses several development tools:

```bash
# Code formatting
black photo_backup.py

# Linting
flake8 photo_backup.py
pylint photo_backup.py

# Security scanning
bandit -r photo_backup.py

# Dependency vulnerability check
safety check
```

### Project Structure

```
photo-backup-script/
├── photo_backup.py          # Main backup script
├── config.example.yaml      # Example configuration
├── requirements.txt         # Runtime dependencies
├── requirements-dev.txt     # Development dependencies
├── setup.py                 # Package setup script
├── pyproject.toml          # Modern Python project configuration
├── tests/                   # Test suite
│   ├── __init__.py
│   └── test_photo_backup.py
├── .github/                 # GitHub Actions workflows
│   └── workflows/
│       └── ci.yml
├── logs/                    # Log files (created at runtime)
├── dist/                    # Built packages (created during build)
├── README.md               # This file
├── CHANGELOG.md            # Version history
├── CONTRIBUTING.md         # Contribution guidelines
└── LICENSE                 # MIT License
```

## CI/CD

This project includes GitHub Actions workflows for automated testing and validation:

### CI Pipeline Features

- **Multi-platform Testing**: Tests on Ubuntu, macOS, and Windows
- **Python Version Matrix**: Tests on Python 3.8, 3.9, 3.10, 3.11, and 3.12
- **Code Quality**: Automated linting with flake8, black, and pylint
- **Security Scanning**: Bandit security analysis and safety dependency checks
- **Build Validation**: Package building and validation with twine
- **Configuration Validation**: YAML syntax checking and README validation
- **Coverage Reporting**: Automated test coverage with Codecov integration

### Workflow Triggers

- Push to main or develop branches
- Pull requests to main or develop branches

## Troubleshooting

### Common Issues

**Permission Denied:**
```
Error: Permission denied when copying to destination
```
**Solution:** Ensure you have read access to source directories and write access to destination directories.

**Disk Full:**
```
Error: No space left on device
```
**Solution:** Check available space on destination drive before running backup. Use `df -h` on Unix-like systems.

**Configuration File Not Found:**
```
Error: Configuration file not found: config.yaml
```
**Solution:** Copy the example configuration: `cp config.example.yaml config.yaml` and edit it.

**Import Error:**
```
ModuleNotFoundError: No module named 'yaml'
```
**Solution:** Install dependencies: `pip install -r requirements.txt`

**Slow Performance:**
Large initial backups may take time. Consider:
- Using `--batch-size` in configuration
- Running during off-peak hours
- Checking network speed if backing up to network storage

### Debug Mode

Enable detailed logging for troubleshooting:
```bash
python photo_backup.py --debug
```

Check logs in `logs/photo_backup.log` for detailed information about each operation.

## Contributing

Contributions are welcome! Please read our [contributing guidelines](CONTRIBUTING.md) for details on:

- Code style and formatting standards
- Testing requirements
- Pull request process
- Issue reporting

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Run tests and linting: `pytest` and `black .`
5. Submit a pull request

## Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history and changes.

### Current Version: 0.2.0

Recent changes include:
- Initial release with core backup functionality
- Content-based deduplication
- Multiple organization strategies
- Comprehensive error handling
- CI/CD pipeline setup

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Roadmap

Planned features for future releases:

- [ ] Cloud storage integration (S3, Google Photos, etc.)
- [ ] Web interface for backup management
- [ ] Automatic photo enhancement during backup
- [ ] Face detection and tagging
- [ ] Mobile app support
- [ ] Real-time backup monitoring
- [ ] Backup scheduling and automation
- [ ] Advanced metadata extraction and organization

## Support

For issues, questions, or contributions:

- **Issues**: [GitHub Issues](https://github.com/AnishShinde-sys/photo-backup-script/issues)
- **Repository**: [GitHub Repository](https://github.com/AnishShinde-sys/photo-backup-script)
- **Documentation**: [Project Wiki](https://github.com/AnishShinde-sys/photo-backup-script/wiki)

## Acknowledgments

- Built with Python 3.8+
- Uses PyYAML for configuration management
- Tested with pytest across multiple platforms
- Security scanning with Bandit and Safety
