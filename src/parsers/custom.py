"""Custom format parser with configurable patterns."""
import re
from typing import Optional, Dict, Any
from .base import BaseParser


class CustomParser(BaseParser):
    """Parser for custom log formats using regex patterns."""

    def __init__(self, pattern: str, field_map: Optional[Dict[str, str]] = None):
        """Initialize with a custom regex pattern.
        
        Args:
            pattern: Regex pattern with named groups
            field_map: Map of regex group names to log entry fields
        """
        self.pattern = re.compile(pattern)
        self.field_map = field_map or {
            'timestamp': 'timestamp',
            'level': 'level',
            'message': 'message'
        }

    def parse(self, line: str, source: str = "") -> Optional[dict]:
        """Parse a log line using custom pattern."""
        match = self.pattern.match(line)
        if not match:
            return None

        groups = match.groupdict()
        entry = {
            'line': line,
            'raw': line,
            'source': source,
            'format': 'custom'
        }

        for group_name, field_name in self.field_map.items():
            if group_name in groups:
                entry[field_name] = groups[group_name]

        if 'level' not in entry:
            entry['level'] = self._extract_level(line)

        if 'timestamp' not in entry:
            entry['timestamp'] = self._extract_timestamp(line)

        if 'message' not in entry:
            entry['message'] = line

        return entry

    def detect(self, line: str) -> bool:
        """Check if line matches custom pattern."""
        return bool(self.pattern.match(line))

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> 'CustomParser':
        """Create parser from configuration dict."""
        pattern = config.get('pattern', '.+')
        field_map = config.get('field_map', {})
        return cls(pattern=pattern, field_map=field_map)
