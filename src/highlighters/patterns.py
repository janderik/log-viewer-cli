"""Custom pattern highlighting."""
import re
from typing import List, Tuple
from .base import BaseHighlighter


class PatternHighlighter(BaseHighlighter):
    """Highlight custom patterns in log entries."""

    def __init__(self, patterns: List[Tuple[str, str]] = None):
        """Initialize with custom patterns.
        
        Args:
            patterns: List of (regex_pattern, color_name) tuples
        """
        self.patterns = []
        if patterns:
            for pattern, color in patterns:
                compiled = re.compile(pattern, re.IGNORECASE)
                self.patterns.append((compiled, color))

        if not self.patterns:
            self.patterns = [
                (re.compile(r'https?://\S+'), 'bright_cyan'),
                (re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'), 'bright_magenta'),
                (re.compile(r'\b\d+\.\d{2,3}ms\b'), 'bright_green'),
                (re.compile(r'\b\d{3}\b(?=\s)'), 'bright_yellow'),
                (re.compile(r'["\'][^"\']+["\']'), 'bright_yellow'),
                (re.compile(r'\b(?:true|false|null|None)\b'), 'magenta'),
                (re.compile(r'\b\d+\b'), 'bright_blue'),
            ]

    def highlight(self, line: str, entry: dict = None) -> str:
        """Highlight custom patterns in the log line."""
        result = line
        for pattern, color in self.patterns:
            result = pattern.sub(lambda m: self._colorize(m.group(), color), result)
        return result

    def add_pattern(self, pattern: str, color: str):
        """Add a new highlighting pattern."""
        compiled = re.compile(pattern, re.IGNORECASE)
        self.patterns.append((compiled, color))
