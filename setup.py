#!/usr/bin/env python3
"""
Setup script for HyperDB - Database with Built-in Blockchain
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join('docs', 'README_HYPERLEDGER.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "HyperDB - Database with Built-in Blockchain"

setup(
    name="hyperdb",
    version="1.0.0",
    author="HyperDB Team",
    author_email="team@hyperdb.com",
    description="Database system with integrated blockchain storage",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/hyperdb",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Database",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "cryptography>=3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "hyperdb=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 