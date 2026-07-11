"""Log buffer management for storing and retrieving log entries."""
from collections import deque
from typing import List, Optional, Iterator


class LogBuffer:
    """Fixed-size circular buffer for log entries."""

    def __init__(self, max_size: int = 10000):
        self.max_size = max_size
        self._buffer: deque = deque(maxlen=max_size)
        self._total_added = 0

    def add(self, entry: dict):
        """Add a log entry to the buffer."""
        self._buffer.append(entry)
        self._total_added += 1

    def get_all(self) -> List[dict]:
        """Get all entries in the buffer."""
        return list(self._buffer)

    def get_recent(self, count: int) -> List[dict]:
        """Get the most recent N entries."""
        return list(self._buffer)[-count:]

    def get_at_index(self, index: int) -> Optional[dict]:
        """Get entry at a specific index."""
        if 0 <= index < len(self._buffer):
            return list(self._buffer)[index]
        return None

    def search(self, pattern: str, case_sensitive: bool = False) -> List[dict]:
        """Search for entries matching a pattern."""
        results = []
        for entry in self._buffer:
            line = entry.get('raw', entry.get('line', ''))
            if case_sensitive and pattern in line:
                results.append(entry)
            elif not case_sensitive and pattern.lower() in line.lower():
                results.append(entry)
        return results

    def filter_by_level(self, level: str) -> List[dict]:
        """Filter entries by log level."""
        return [e for e in self._buffer if e.get('level', '').upper() == level.upper()]

    def clear(self):
        """Clear the buffer."""
        self._buffer.clear()

    @property
    def size(self) -> int:
        """Current number of entries in the buffer."""
        return len(self._buffer)

    @property
    def total_added(self) -> int:
        """Total entries ever added."""
        return self._total_added

    @property
    def is_full(self) -> bool:
        """Check if buffer is at capacity."""
        return len(self._buffer) == self.max_size

    def __iter__(self) -> Iterator[dict]:
        return iter(self._buffer)

    def __len__(self) -> int:
        return len(self._buffer)

    def __getitem__(self, index: int) -> dict:
        return list(self._buffer)[index]
