# Contributing to Photo Backup Script

Thank you for your interest in contributing to the Photo Backup Script! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### Setting Up Development Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/photo-backup-script.git
   cd photo-backup-script
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Run tests:**
   ```bash
   pytest
   ```

## Code Style and Quality

This project uses several tools to maintain code quality:

### Code Formatting with Black

```bash
# Format code
black photo_backup.py

# Check formatting without making changes
black --check photo_backup.py
```

### Linting with Flake8

```bash
flake8 photo_backup.py
```

### Advanced Linting with Pylint

```bash
pylint photo_backup.py
```

### Security Scanning with Bandit

```bash
bandit -r photo_backup.py
```

### Dependency Vulnerability Check

```bash
safety check
```

## Testing

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=photo_backup --cov-report=html
```

### Run Specific Test

```bash
pytest tests/test_photo_backup.py::test_specific_function
```

## Continuous Integration

This project uses GitHub Actions for continuous integration:

- **CI Workflow**: Runs on every push and pull request
  - Tests on multiple Python versions (3.8-3.12)
  - Tests on multiple operating systems (Linux, macOS, Windows)
  - Runs linting, formatting checks, and security scans
  - Validates configuration and documentation

- **Release Workflow**: Runs on version tags
  - Builds distribution packages
  - Creates GitHub releases

### CI Status

Before submitting a pull request, ensure all CI checks pass. You can run the same checks locally:

```bash
# Run basic checks
python photo_backup.py --help
python photo_backup.py --dry-run --config config.example.yaml

# Run linting
flake8 photo_backup.py --count --select=E9,F63,F7,F82 --show-source --statistics
black --check photo_backup.py
pylint photo_backup.py --exit-zero

# Run security checks
bandit -r photo_backup.py
safety check
```

## Making Changes

### Branch Strategy

1. Create a new branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

3. Push to your fork and create a pull request

### Commit Messages

Use clear, descriptive commit messages:

```
fix: Resolve issue with duplicate file detection

- Improved hash comparison algorithm
- Added logging for debugging
- Updated tests

Closes #123
```

### Pull Request Guidelines

- Ensure all CI checks pass
- Update documentation if needed
- Add tests for new functionality
- Keep changes focused and minimal
- Reference related issues

## Adding Features

When adding new features:

1. Update the README if user-facing
2. Add appropriate tests
3. Update CHANGELOG.md
4. Consider backward compatibility
5. Document any configuration changes

## Bug Fixes

When fixing bugs:

1. Add a test that reproduces the bug
2. Fix the issue
3. Ensure the test now passes
4. Update CHANGELOG.md

## Documentation

- Keep README.md up to date
- Document new features
- Update examples as needed
- Ensure code is well-commented

## Questions or Issues?

- Open an issue on GitHub for bugs or feature requests
- Check existing issues before creating new ones
- Be descriptive and provide steps to reproduce

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to the Photo Backup Script!
