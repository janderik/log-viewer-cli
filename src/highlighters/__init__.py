"""Syntax highlighting system."""
from .base import BaseHighlighter
from .log_level import LogLevelHighlighter
from .timestamp import TimestampHighlighter
from .patterns import PatternHighlighter

__all__ = ['BaseHighlighter', 'LogLevelHighlighter', 'TimestampHighlighter', 'PatternHighlighter']
