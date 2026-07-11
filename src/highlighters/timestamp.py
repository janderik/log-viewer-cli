"""Timestamp syntax highlighting."""
import re
from .base import BaseHighlighter


class TimestampHighlighter(BaseHighlighter):
    """Highlight timestamps in log entries."""

    TIMESTAMP_PATTERNS = [
        re.compile(r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?'),
        re.compile(r'\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}'),
        re.compile(r'\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}'),
        re.compile(r'\d{4}/\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2}'),
    ]

    def highlight(self, line: str, entry: dict = None) -> str:
        """Highlight timestamps in the log line."""
        result = line
        for pattern in self.TIMESTAMP_PATTERNS:
            result = pattern.sub(lambda m: self._colorize(m.group(), 'cyan'), result)
        return result
