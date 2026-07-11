"""Regex-based log filters."""
import re
from typing import Optional
from .base import BaseFilter


class RegexFilter(BaseFilter):
    """Filter log entries using regular expressions."""

    def __init__(self, pattern: str, case_sensitive: bool = False, field: Optional[str] = None):
        """Initialize regex filter.
        
        Args:
            pattern: Regex pattern to match
            case_sensitive: Whether regex is case sensitive
            field: Specific field to match against
        """
        flags = 0 if case_sensitive else re.IGNORECASE
        self.regex = re.compile(pattern, flags)
        self.pattern = pattern
        self.case_sensitive = case_sensitive
        self.field = field

    def matches(self, entry: dict) -> bool:
        """Check if entry matches the regex pattern."""
        if self.field:
            value = str(entry.get(self.field, ''))
        else:
            value = entry.get('raw', entry.get('line', ''))

        return bool(self.regex.search(value))

    def get_matches(self, entry: dict) -> list:
        """Get all matches in an entry."""
        if self.field:
            value = str(entry.get(self.field, ''))
        else:
            value = entry.get('raw', entry.get('line', ''))

        return self.regex.findall(value)

    @classmethod
    def from_query(cls, query: str) -> 'RegexFilter':
        """Create filter from a regex query string.
        
        Supports:
            - Simple regex: "timeout|refused"
            - Negated regex: "!(healthcheck|ping)"
            - Field-specific: "message:\\d{3}ms"
        """
        if query.startswith('!'):
            inner = query[1:]
            filter_obj = cls(inner)
            return NegateRegexFilter(filter_obj)

        if ':' in query:
            field, pattern = query.split(':', 1)
            return cls(pattern=pattern, field=field)

        return cls(pattern=query)


class NegateRegexFilter(BaseFilter):
    """Negated regex filter."""

    def __init__(self, filter_obj: RegexFilter):
        self.filter_obj = filter_obj

    def matches(self, entry: dict) -> bool:
        return not self.filter_obj.matches(entry)
