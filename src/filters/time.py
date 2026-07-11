"""Time-based log filters."""
from datetime import datetime, timedelta
from typing import Optional
from .base import BaseFilter


class TimeFilter(BaseFilter):
    """Filter log entries by timestamp."""

    def __init__(self, since: Optional[datetime] = None, until: Optional[datetime] = None):
        """Initialize time filter.
        
        Args:
            since: Include entries after this time
            until: Include entries until this time
        """
        self.since = since
        self.until = until

    def matches(self, entry: dict) -> bool:
        """Check if entry timestamp is within the specified range."""
        timestamp_str = entry.get('timestamp')
        if not timestamp_str:
            return True

        try:
            timestamp = self._parse_timestamp(timestamp_str)
        except ValueError:
            return True

        if self.since and timestamp < self.since:
            return False
        if self.until and timestamp > self.until:
            return False
        return True

    def _parse_timestamp(self, ts: str) -> datetime:
        """Parse various timestamp formats."""
        formats = [
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d %H:%M:%S',
            '%d/%b/%Y:%H:%M:%S',
            '%b %d %H:%M:%S',
        ]
        for fmt in formats:
            try:
                return datetime.strptime(ts, fmt)
            except ValueError:
                continue
        raise ValueError(f"Cannot parse timestamp: {ts}")

    @classmethod
    def from_query(cls, query: str) -> 'TimeFilter':
        """Create filter from a time query string.
        
        Supports:
            - Relative time: "1h", "30m", "7d"
            - Named periods: "today", "yesterday"
            - ISO timestamp: "2024-01-01T10:00:00"
            - Date only: "2024-01-01"
        """
        now = datetime.now()

        query = query.lower().strip()

        if query == 'today':
            since = now.replace(hour=0, minute=0, second=0, microsecond=0)
            return cls(since=since)
        elif query == 'yesterday':
            since = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            until = now.replace(hour=0, minute=0, second=0, microsecond=0)
            return cls(since=since, until=until)
        elif query.endswith('m'):
            minutes = int(query[:-1])
            return cls(since=now - timedelta(minutes=minutes))
        elif query.endswith('h'):
            hours = int(query[:-1])
            return cls(since=now - timedelta(hours=hours))
        elif query.endswith('d'):
            days = int(query[:-1])
            return cls(since=now - timedelta(days=days))
        else:
            try:
                ts = datetime.fromisoformat(query)
                return cls(since=ts)
            except ValueError:
                pass

        return cls()


class NegateTimeFilter(BaseFilter):
    """Negated time filter."""

    def __init__(self, filter_obj: TimeFilter):
        self.filter_obj = filter_obj

    def matches(self, entry: dict) -> bool:
        return not self.filter_obj.matches(entry)
