# Photo Backup Script

Automated photo backup and synchronization tool for organizing and preserving your digital photo collection.

## Overview

The Photo Backup Script provides a reliable way to backup photos from various sources (cameras, phones, external drives) to organized storage locations with automatic deduplication, metadata preservation, and optional cloud synchronization.

## Features

- **Automated Detection**: Automatically detects and backs up new photos from specified source directories
- **Intelligent Organization**: Organizes photos by date, location, or custom folder structures
- **Deduplication**: Prevents duplicate files using content-based hashing
- **Metadata Preservation**: Maintains EXIF data, timestamps, and other photo metadata
- **Incremental Backups**: Only processes new or modified files for efficiency
- **Cross-Platform Support**: Works on macOS, Linux, and Windows
- **Configurable**: Flexible configuration options for different backup strategies

## Installation

### Prerequisites

- Python 3.7 or higher
- rsync (for efficient file copying)
- Optional: exiftool for advanced metadata handling

### Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/photo-backup-script.git
cd photo-backup-script
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your backup settings:
```bash
cp config.example.yaml config.yaml
# Edit config.yaml with your source and destination paths
```

## Usage

### Basic Backup

```bash
python photo_backup.py
```

### Advanced Options

```bash
# Dry run to see what would be backed up
python photo_backup.py --dry-run

# Backup from specific source
python photo_backup.py --source /path/to/photos

# Verbose output
python photo_backup.py --verbose

# Force full re-scan
python photo_backup.py --force-rescan
```

## Configuration

Edit `config.yaml` to customize your backup behavior:

```yaml
sources:
  - path: "/Users/username/Pictures/Camera"
    recursive: true
    file_types: ["jpg", "jpeg", "png", "raw", "heic"]

destination:
  path: "/Volumes/BackupDrive/Photos"
  organization: "date"  # options: date, flat, custom
  date_format: "%Y/%m/%d"

options:
  deduplicate: true
  preserve_metadata: true
  verify_checksums: true
  max_file_size_mb: 100
```

## Organization Strategies

### Date-based (Default)
```
destination/
├── 2023/
│   ├── 01/
│   │   ├── 15/
│   │   │   ├── photo1.jpg
│   │   │   └── photo2.jpg
```

### Flat Structure
```
destination/
├── photo1_20230115.jpg
├── photo2_20230115.jpg
```

### Custom Structure
Configure your own folder hierarchy using date variables and metadata fields.

## Troubleshooting

### Common Issues

**Permission Denied**: Ensure you have read access to source directories and write access to destination.

**Disk Full**: Check available space on destination drive before running backup.

**Slow Performance**: Large initial backups may take time. Consider using `--batch-size` to process files in chunks.

### Debug Mode

Enable debug logging:
```bash
python photo_backup.py --debug
```

Check logs in `logs/photo_backup.log` for detailed information.

## CI/CD

This project includes GitHub Actions workflows for automated testing and validation. See `.github/workflows/` for details.

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests to the main branch.

## License

MIT License - see LICENSE file for details

## Roadmap

- [ ] Cloud storage integration (S3, Google Photos, etc.)
- [ ] Web interface for backup management
- [ ] Automatic photo enhancement during backup
- [ ] Face detection and tagging
- [ ] Mobile app support

## Support

For issues, questions, or contributions, please open an issue on GitHub or contact [your-email@example.com].
