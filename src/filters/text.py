"""Text-based log filters."""
from typing import Optional
from .base import BaseFilter


class TextFilter(BaseFilter):
    """Filter log entries by text content."""

    def __init__(self, text: str, case_sensitive: bool = False, field: Optional[str] = None):
        """Initialize text filter.
        
        Args:
            text: Text to search for
            case_sensitive: Whether search is case sensitive
            field: Specific field to search in (None for full line)
        """
        self.text = text
        self.case_sensitive = case_sensitive
        self.field = field

    def matches(self, entry: dict) -> bool:
        """Check if entry contains the specified text."""
        if self.field:
            value = str(entry.get(self.field, ''))
        else:
            value = entry.get('raw', entry.get('line', ''))

        if self.case_sensitive:
            return self.text in value
        else:
            return self.text.lower() in value.lower()

    @classmethod
    def from_query(cls, query: str) -> 'TextFilter':
        """Create filter from a query string.
        
        Supports:
            - Simple text: "error"
            - Negated text: "!error"
            - Field-specific: "message:timeout"
        """
        if query.startswith('!'):
            filter_obj = cls(query[1:])
            return NegateTextFilter(filter_obj)

        if ':' in query:
            field, text = query.split(':', 1)
            return cls(text=text, field=field)

        return cls(text=query)


class NegateTextFilter(BaseFilter):
    """Negated text filter."""

    def __init__(self, filter_obj: TextFilter):
        self.filter_obj = filter_obj

    def matches(self, entry: dict) -> bool:
        return not self.filter_obj.matches(entry)
