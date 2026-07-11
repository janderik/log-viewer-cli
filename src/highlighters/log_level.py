"""Log level syntax highlighting."""
import re
from .base import BaseHighlighter


class LogLevelHighlighter(BaseHighlighter):
    """Highlight log entries based on their severity level."""

    LEVEL_COLORS = {
        'ERROR': 'bright_red',
        'CRITICAL': 'bright_red',
        'FATAL': 'bright_red',
        'WARN': 'bright_yellow',
        'WARNING': 'bright_yellow',
        'INFO': 'bright_green',
        'DEBUG': 'gray',
    }

    LEVEL_PATTERNS = {
        'ERROR': re.compile(r'\b(ERROR|CRITICAL|FATAL|Exception|Traceback)\b', re.IGNORECASE),
        'WARN': re.compile(r'\b(WARN|WARNING)\b', re.IGNORECASE),
        'INFO': re.compile(r'\b(INFO)\b', re.IGNORECASE),
        'DEBUG': re.compile(r'\b(DEBUG)\b', re.IGNORECASE),
    }

    def highlight(self, line: str, entry: dict = None) -> str:
        """Highlight based on log level."""
        if entry:
            level = entry.get('level', '').upper()
            if level in self.LEVEL_COLORS:
                return self._colorize(line, self.LEVEL_COLORS[level])

        for level, pattern in self.LEVEL_PATTERNS.items():
            if pattern.search(line):
                return self._colorize(line, self.LEVEL_COLORS[level])

        return line
