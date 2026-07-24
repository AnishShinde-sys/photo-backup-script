#!/usr/bin/env python3
"""
Setup script for photo-backup-script
"""

from setuptools import setup, find_packages

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="photo-backup-script",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    author="Your Name",
    author_email="your-email@example.com",
    description="Automated photo backup and synchronization tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/photo-backup-script",
    py_modules=["photo_backup"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Archiving :: Backup",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "flake8>=6.0.0",
            "black>=23.0.0",
            "pylint>=2.17.0",
            "bandit>=1.7.0",
            "safety>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "photo-backup=photo_backup:main",
        ],
    },
)
