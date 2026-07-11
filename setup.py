from setuptools import setup, find_packages

setup(
    name="log-viewer-cli",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "rich>=12.0.0",
        "pyyaml>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "logview=cli:main",
        ],
    },
    author="janderik",
    description="Terminal log viewer with filtering and highlighting",
    python_requires=">=3.8",
)
