"""Log level filters."""
from typing import List
from .base import BaseFilter


class LevelFilter(BaseFilter):
    """Filter log entries by severity level."""

    LEVEL_HIERARCHY = {
        'DEBUG': 0,
        'INFO': 1,
        'WARN': 2,
        'ERROR': 3,
        'CRITICAL': 4
    }

    def __init__(self, levels: List[str], min_level: bool = False):
        """Initialize level filter.
        
        Args:
            levels: List of log levels to include
            min_level: If True, include all levels at or above the minimum
        """
        self.levels = [l.upper() for l in levels]
        self.min_level = min_level
        if self.min_level and self.levels:
            self._min_value = self.LEVEL_HIERARCHY.get(self.levels[0], 0)
        else:
            self._min_value = 0

    def matches(self, entry: dict) -> bool:
        """Check if entry matches the level filter."""
        level = entry.get('level', 'UNKNOWN').upper()

        if level not in self.LEVEL_HIERARCHY:
            return False

        if self.min_level:
            return self.LEVEL_HIERARCHY[level] >= self._min_value
        else:
            return level in self.levels

    @classmethod
    def from_query(cls, query: str) -> 'LevelFilter':
        """Create filter from a level query string.
        
        Supports:
            - Single level: "ERROR"
            - Multiple levels: "ERROR,WARN"
            - Minimum level: ">=INFO" or ">WARN"
            - Negated: "!DEBUG"
        """
        if query.startswith('!'):
            inner = query[1:]
            filter_obj = cls([inner])
            return NegateLevelFilter(filter_obj)

        if query.startswith('>='):
            return cls([query[2:]], min_level=True)
        elif query.startswith('>'):
            levels = list(cls.LEVEL_HIERARCHY.keys())
            min_idx = levels.index(query[1:].upper()) if query[1:].upper() in levels else 0
            return cls(levels[min_idx + 1:], min_level=True)

        if ',' in query:
            levels = [l.strip() for l in query.split(',')]
        else:
            levels = [query]

        return cls(levels)


class NegateLevelFilter(BaseFilter):
    """Negated level filter."""

    def __init__(self, filter_obj: LevelFilter):
        self.filter_obj = filter_obj

    def matches(self, entry: dict) -> bool:
        return not self.filter_obj.matches(entry)
