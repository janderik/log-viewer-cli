"""JSON log format parser."""
import json
from typing import Optional
from .base import BaseParser


class JsonParser(BaseParser):
    """Parser for JSON-formatted log lines."""

    LEVEL_FIELDS = ['level', 'severity', 'log_level', 'loglevel', 'log.level']
    TIMESTAMP_FIELDS = ['timestamp', 'time', 'ts', 'datetime', 'date', '@timestamp']
    MESSAGE_FIELDS = ['message', 'msg', 'log', 'text']

    def parse(self, line: str, source: str = "") -> Optional[dict]:
        """Parse a JSON log line."""
        try:
            data = json.loads(line)
            if not isinstance(data, dict):
                return None

            level = 'UNKNOWN'
            for field in self.LEVEL_FIELDS:
                if field in data:
                    level = str(data[field]).upper()
                    break

            timestamp = None
            for field in self.TIMESTAMP_FIELDS:
                if field in data:
                    timestamp = str(data[field])
                    break

            message = ''
            for field in self.MESSAGE_FIELDS:
                if field in data:
                    message = str(data[field])
                    break

            return {
                'line': json.dumps(data, indent=2),
                'raw': line,
                'source': source,
                'timestamp': timestamp,
                'level': level,
                'message': message,
                'data': data,
                'format': 'json'
            }
        except json.JSONDecodeError:
            return None

    def detect(self, line: str) -> bool:
        """Check if line is valid JSON."""
        try:
            data = json.loads(line)
            return isinstance(data, dict)
        except (json.JSONDecodeError, ValueError):
            return False
