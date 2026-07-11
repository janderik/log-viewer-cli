"""Base parser interface for log formats."""
from abc import ABC, abstractmethod
from typing import Optional


class BaseParser(ABC):
    """Abstract base class for log parsers."""

    @abstractmethod
    def parse(self, line: str, source: str = "") -> Optional[dict]:
        """Parse a log line into a structured entry.
        
        Args:
            line: Raw log line text
            source: Source file or identifier
            
        Returns:
            Parsed log entry dict or None if line cannot be parsed
        """
        pass

    def detect(self, line: str) -> bool:
        """Detect if this parser can handle the given line format."""
        return True

    def _extract_timestamp(self, line: str) -> Optional[str]:
        """Extract timestamp from log line."""
        import re
        patterns = [
            r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}',
            r'\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}',
            r'\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}',
        ]
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                return match.group(0)
        return None

    def _extract_level(self, line: str) -> str:
        """Extract log level from line."""
        upper = line.upper()
        if 'CRITICAL' in upper or 'FATAL' in upper:
            return 'ERROR'
        elif 'ERROR' in upper:
            return 'ERROR'
        elif 'WARN' in upper:
            return 'WARN'
        elif 'INFO' in upper:
            return 'INFO'
        elif 'DEBUG' in upper:
            return 'DEBUG'
        return 'UNKNOWN'
