#!/usr/bin/env python3
"""Setup configuration for CP437 Telnet Client."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cp437-telnet",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A telnet client with CP437 graphical character support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cp437-telnet",
    py_modules=["cp437_telnet"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: System :: Networking",
        "Topic :: Communications :: Conferencing",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=[
        "telnetlib3>=1.0.4",
    ],
    entry_points={
        "console_scripts": [
            "cp437-telnet=cp437_telnet:main",
        ],
    },
)
