import sys
import argparse
import hashlib
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Set
import json

# Global logger that will be configured in main()
logger = None


class PhotoBackup:
    """Main photo backup class handling file detection, deduplication, and copying."""

    def __init__(self, config: Dict):
        self.config = config
        self.backup_stats = {
            "processed": 0,
            "copied": 0,
            "skipped": 0,
            "errors": 0,
            "bytes_saved": 0,
            "removed": 0,
        }
        self.state_file = None
        self.backup_state = {"files": {}, "last_run": None}
        self.current_file_hashes = {}  # Track current files by hash for move detection

    def calculate_file_hash(self, filepath: Path) -> str:
        """Calculate SHA256 hash of a file for deduplication."""
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating hash for {filepath}: {e}")
            return ""

    def get_file_date(self, filepath: Path) -> datetime:
        """Extract creation or modified date from file."""
        try:
            # Try to get creation date first, then modified date
            stat = filepath.stat()
            timestamp = stat.st_ctime if hasattr(stat, "st_ctime") else stat.st_mtime
            return datetime.fromtimestamp(timestamp)
        except Exception as e:
            logger.error(f"Error getting date for {filepath}: {e}")
            return datetime.now()

    def get_file_signature(self, filepath: Path) -> Dict:
        """Get file signature for incremental backup tracking."""
        try:
            stat = filepath.stat()
            return {
                "size": stat.st_size,
                "mtime": stat.st_mtime,
                "hash": self.calculate_file_hash(filepath),
            }
        except Exception as e:
            logger.error(f"Error getting signature for {filepath}: {e}")
            return {}

    def load_backup_state(self, state_file: Path):
        """Load the backup state from state file."""
        if state_file.exists():
            try:
                with open(state_file, "r") as f:
                    self.backup_state = json.load(f)
                logger.debug(
                    f"Loaded backup state with {len(self.backup_state.get('files', {}))} tracked files"
                )
            except Exception as e:
                logger.warning(f"Could not load backup state: {e}")
                self.backup_state = {"files": {}, "last_run": None}
        else:
            self.backup_state = {"files": {}, "last_run": None}

    def save_backup_state(self, state_file: Path):
        """Save the backup state to state file."""
        try:
            state_file.parent.mkdir(parents=True, exist_ok=True)
            with open(state_file, "w") as f:
                self.backup_state["last_run"] = datetime.now().isoformat()
                json.dump(self.backup_state, f, indent=2)
            logger.debug(
                f"Saved backup state with {len(self.backup_state.get('files', {}))} tracked files"
            )
        except Exception as e:
            logger.error(f"Could not save backup state: {e}")

    def is_file_unchanged(self, source_file: Path, file_record: Dict) -> bool:
        """Check if file has changed since last backup."""
        try:
            stat = source_file.stat()
            # Quick check: size and mtime
            if stat.st_size == file_record.get("size") and stat.st_mtime == file_record.get(
                "mtime"
            ):
                return True
            # Deep check: hash comparison
            current_hash = self.calculate_file_hash(source_file)
            return current_hash == file_record.get("hash")
        except Exception:
            return False

    def is_duplicate(self, filepath: Path, destination_dir: Path) -> bool:
        """Check if file already exists in destination based on hash."""
        if not self.config.get("options", {}).get("deduplicate", True):
            return False

        file_hash = self.calculate_file_hash(filepath)
        if not file_hash:
            return False

        # Check if any file in destination has same hash
        for existing_file in destination_dir.rglob("*"):
            if existing_file.is_file():
                existing_hash = self.calculate_file_hash(existing_file)
                if existing_hash == file_hash:
                    logger.info(f"Duplicate found: {filepath.name} (matches {existing_file})")
                    return True

        return False

    def get_destination_path(self, source_file: Path) -> Path:
        """Generate destination path based on organization strategy."""
        dest_base = Path(self.config["destination"]["path"])
        organization = self.config["destination"].get("organization", "date")

        if organization == "date":
            date = self.get_file_date(source_file)
            date_format = self.config["destination"].get("date_format", "%Y/%m/%d")
            date_path = date.strftime(date_format)
            return dest_base / date_path / source_file.name

        elif organization == "flat":
            return dest_base / source_file.name

        else:  # custom or other
            return dest_base / source_file.name

    def backup_file(self, source_file: Path, args) -> bool:
        """Backup a single file to destination."""
        try:
            self.backup_stats["processed"] += 1

            # Check file size limit
            max_size = self.config.get("options", {}).get("max_file_size_mb", 100) * 1024 * 1024
            if source_file.stat().st_size > max_size:
                logger.info(f"Skipping {source_file.name}: exceeds size limit")
                self.backup_stats["skipped"] += 1
                return False

            # Get destination path
            dest_path = self.get_destination_path(source_file)

            # Create destination directories if needed
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # Check if file is unchanged (incremental backup)
            source_str = str(source_file)
            if not args.force_rescan and source_str in self.backup_state["files"]:
                if self.is_file_unchanged(source_file, self.backup_state["files"][source_str]):
                    logger.debug(f"Skipping unchanged file: {source_file.name}")
                    self.backup_stats["skipped"] += 1
                    return True

            # Check for duplicates
            if self.is_duplicate(source_file, dest_path.parent):
                # Record as backed up even if duplicate (to avoid re-checking)
                self.backup_state["files"][source_str] = self.get_file_signature(source_file)
                self.backup_state["files"][source_str]["dest_path"] = str(dest_path)
                self.backup_stats["skipped"] += 1
                return False

            # Copy file
            if args.dry_run:
                logger.info(f"[DRY RUN] Would copy: {source_file} -> {dest_path}")
                return True

            shutil.copy2(source_file, dest_path)
            logger.info(f"Copied: {source_file.name}")
            self.backup_stats["copied"] += 1
            self.backup_stats["bytes_saved"] += source_file.stat().st_size

            # Record in backup state
            self.backup_state["files"][source_str] = self.get_file_signature(source_file)
            self.backup_state["files"][source_str]["dest_path"] = str(dest_path)

            return True

        except Exception as e:
            logger.error(f"Error backing up {source_file}: {e}")
            self.backup_stats["errors"] += 1
            return False

    def scan_directory(self, directory: Path, file_types: List[str]) -> List[Path]:
        """Scan directory for photo files."""
        photo_files = []
        recursive = self.config.get("sources", [{}])[0].get("recursive", True)

        pattern = "**/*" if recursive else "*"
        for file_path in directory.glob(pattern):
            if file_path.is_file():
                # Check file extension
                if file_path.suffix.lower().lstrip(".") in file_types:
                    photo_files.append(file_path)

        return sorted(photo_files)

    def sync_deletions(self, source_files: List[Path], dest_base: Path) -> int:
        """Remove files from destination that no longer exist in source (two-way sync)."""
        if not self.config.get("options", {}).get("sync_deletions", False):
            return 0

        source_paths = {str(f) for f in source_files}
        removed_count = 0

        # Find files in state that are no longer in source
        for source_path, record in list(self.backup_state["files"].items()):
            if source_path not in source_paths:
                dest_path = record.get("dest_path")
                if dest_path and Path(dest_path).exists():
                    try:
                        if self.args.dry_run:
                            logger.info(f"[DRY RUN] Would remove: {dest_path}")
                        else:
                            Path(dest_path).unlink()
                            logger.info(f"Removed (source deleted): {dest_path}")
                        removed_count += 1
                    except Exception as e:
                        logger.error(f"Error removing {dest_path}: {e}")
                # Remove from state regardless of whether file existed
                del self.backup_state["files"][source_path]

        return removed_count

    def run_backup(self, args):
        """Execute the backup process."""
        self.args = args

        logger.info("Starting photo backup process")
        logger.info(f"Source: {self.config['sources'][0]['path']}")
        logger.info(f"Destination: {self.config['destination']['path']}")

        # Get source configuration
        source_config = self.config["sources"][0]
        source_path = Path(source_config["path"])
        file_types = source_config.get("file_types", ["jpg", "jpeg", "png", "raw", "heic"])

        # Validate paths
        if not source_path.exists():
            logger.error(f"Source directory does not exist: {source_path}")
            return False

        # Create destination base directory
        dest_base = Path(self.config["destination"]["path"])
        dest_base.mkdir(parents=True, exist_ok=True)

        # Load backup state for incremental backups
        state_file = dest_base / ".photo_backup_state.json"
        if not args.force_rescan:
            self.load_backup_state(state_file)
        else:
            logger.info("Force rescan enabled - starting fresh")
            self.backup_state = {"files": {}, "last_run": None}

        # Scan for files
        logger.info("Scanning for photo files...")
        photo_files = self.scan_directory(source_path, file_types)
        logger.info(f"Found {len(photo_files)} photo files")

        # Backup files
        for photo_file in photo_files:
            self.backup_file(photo_file, args)

        # Sync deletions if enabled
        removed = self.sync_deletions(photo_files, dest_base)
        self.backup_stats["removed"] = removed

        # Save backup state
        if not args.dry_run:
            self.save_backup_state(state_file)

        # Print summary
        self.print_summary()
        return True

    def print_summary(self):
        """Print backup summary statistics."""
        logger.info("=" * 50)
        logger.info("BACKUP SUMMARY")
        logger.info("=" * 50)
        logger.info(f"Files processed: {self.backup_stats['processed']}")
        logger.info(f"Files copied: {self.backup_stats['copied']}")
        logger.info(f"Files skipped (unchanged/duplicates/size): {self.backup_stats['skipped']}")
        logger.info(f"Files removed (sync): {self.backup_stats['removed']}")
        logger.info(f"Errors: {self.backup_stats['errors']}")
        logger.info(f"Total bytes saved: {self.backup_stats['bytes_saved']:,}")
        logger.info("=" * 50)


def setup_logging(debug: bool = False, verbose: bool = False):
    """Configure logging after logs directory is created."""
    import logging

    global logger

    # Determine log level
    if debug:
        log_level = logging.DEBUG
    elif verbose:
        log_level = logging.INFO
    else:
        log_level = logging.INFO

    # Configure logging
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("logs/photo_backup.log"), logging.StreamHandler(sys.stdout)],
    )
    logger = logging.getLogger(__name__)


def load_config(config_path: str) -> Dict:
    """Load configuration from YAML or JSON file."""
    config_file = Path(config_path)

    if not config_file.exists():
        logger.error(f"Configuration file not found: {config_path}")
        sys.exit(1)

    try:
        with open(config_file, "r") as f:
            if config_file.suffix in [".yaml", ".yml"]:
                import yaml

                return yaml.safe_load(f)
            elif config_file.suffix == ".json":
                return json.load(f)
            else:
                logger.error("Unsupported configuration file format")
                sys.exit(1)
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        sys.exit(1)


def main():
    """Main entry point for the photo backup script."""
    parser = argparse.ArgumentParser(description="Photo Backup Script v0.2")
    parser.add_argument("--config", "-c", default="config.yaml", help="Path to configuration file")
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Show what would be backed up without actually copying",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--source", "-s", help="Override source directory")
    parser.add_argument(
        "--force-rescan", action="store_true", help="Force full re-scan of source directory"
    )

    args = parser.parse_args()

    # Create logs directory first, before setting up logging
    Path("logs").mkdir(exist_ok=True)

    # Now set up logging with the logs directory available
    setup_logging(debug=args.debug, verbose=args.verbose)

    # Load configuration
    config = load_config(args.config)

    # Override source if specified
    if args.source:
        config["sources"][0]["path"] = args.source

    # Create backup instance and run
    backup = PhotoBackup(config)
    success = backup.run_backup(args)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
