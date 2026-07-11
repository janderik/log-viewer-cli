"""Apache/Nginx log format parser."""
import re
from typing import Optional
from .base import BaseParser


class ApacheParser(BaseParser):
    """Parser for Apache/Nginx combined log format."""

    # Combined Log Format: 127.0.0.1 - - [01/Jan/2024:12:00:00 +0000] "GET /path HTTP/1.1" 200 1234 "referer" "user-agent"
    COMBINED_PATTERN = re.compile(
        r'^(?P<ip>\S+)\s+'
        r'(?P<ident>\S+)\s+'
        r'(?P<user>\S+)\s+'
        r'\[(?P<timestamp>[^\]]+)\]\s+'
        r'"(?P<method>\S+)\s+(?P<path>\S+)\s+(?P<protocol>[^"]+)"\s+'
        r'(?P<status>\d{3})\s+'
        r'(?P<size>\S+)'
        r'(?:\s+"(?P<referer>[^"]*)"\s+"(?P<useragent>[^"]*)")?'
    )

    def parse(self, line: str, source: str = "") -> Optional[dict]:
        """Parse an Apache/Nginx log line."""
        match = self.COMBINED_PATTERN.match(line)
        if match:
            status = int(match.group('status'))
            level = self._status_to_level(status)
            return {
                'line': line,
                'raw': line,
                'source': source,
                'timestamp': match.group('timestamp'),
                'ip': match.group('ip'),
                'method': match.group('method'),
                'path': match.group('path'),
                'protocol': match.group('protocol'),
                'status': status,
                'size': match.group('size'),
                'referer': match.group('referer'),
                'useragent': match.group('useragent'),
                'level': level,
                'message': f"{match.group('method')} {match.group('path')} {status}",
                'format': 'apache-combined'
            }
        return None

    def _status_to_level(self, status: int) -> str:
        """Convert HTTP status to log level."""
        if status >= 500:
            return 'ERROR'
        elif status >= 400:
            return 'WARN'
        elif status >= 300:
            return 'INFO'
        else:
            return 'INFO'

    def detect(self, line: str) -> bool:
        """Check if line matches Apache combined format."""
        return bool(self.COMBINED_PATTERN.match(line))
