"""Main log viewing engine."""
import os
import time
from typing import List, Optional, Callable
from .buffer import LogBuffer
from .display import Display
from ..parsers.base import BaseParser
from ..filters.base import BaseFilter
from ..highlighters.base import BaseHighlighter


class LogViewer:
    """Core engine for viewing and monitoring log files."""

    def __init__(
        self,
        files: List[str],
        follow: bool = False,
        parser: Optional[BaseParser] = None,
        filters: Optional[List[BaseFilter]] = None,
        highlighters: Optional[List[BaseHighlighter]] = None,
        theme: str = "default",
        buffer_size: int = 10000
    ):
        self.files = files
        self.follow = follow
        self.parser = parser
        self.filters = filters or []
        self.highlighters = highlighters or []
        self.theme = theme
        self.buffer_size = buffer_size
        self.buffer = LogBuffer(buffer_size)
        self.display = Display(theme)
        self._running = False
        self._paused = False
        self._bookmarks: List[int] = []
        self._file_positions: dict = {}
        self._callbacks: List[Callable] = []

    def add_callback(self, callback: Callable):
        """Add a callback for log entry events."""
        self._callbacks.append(callback)

    def _notify_callbacks(self, entry):
        """Notify all callbacks of a new log entry."""
        for callback in self._callbacks:
            callback(entry)

    def load_files(self):
        """Load initial content from all files."""
        for filepath in self.files:
            if not os.path.exists(filepath):
                print(f"Warning: File not found: {filepath}")
                continue
            self._load_file(filepath)

    def _load_file(self, filepath: str):
        """Load content from a single file."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
                for line in lines[-self.buffer_size:]:
                    entry = self._parse_line(line.strip(), filepath)
                    if entry and self._apply_filters(entry):
                        self.buffer.add(entry)
                        self._notify_callbacks(entry)
                self._file_positions[filepath] = f.tell()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")

    def _parse_line(self, line: str, source: str = "") -> Optional[dict]:
        """Parse a log line into a structured entry."""
        if self.parser:
            return self.parser.parse(line, source)
        return {
            'line': line,
            'source': source,
            'level': self._detect_level(line),
            'timestamp': None,
            'raw': line
        }

    def _detect_level(self, line: str) -> str:
        """Detect log level from line content."""
        upper = line.upper()
        if 'ERROR' in upper or 'CRITICAL' in upper or 'FATAL' in upper:
            return 'ERROR'
        elif 'WARN' in upper:
            return 'WARN'
        elif 'INFO' in upper:
            return 'INFO'
        elif 'DEBUG' in upper:
            return 'DEBUG'
        return 'UNKNOWN'

    def _apply_filters(self, entry: dict) -> bool:
        """Apply all filters to a log entry."""
        for filter_obj in self.filters:
            if not filter_obj.matches(entry):
                return False
        return True

    def _apply_highlighting(self, entry: dict) -> str:
        """Apply highlighting to a log entry."""
        line = entry.get('line', entry.get('raw', ''))
        for highlighter in self.highlighters:
            line = highlighter.highlight(line, entry)
        return line

    def start(self):
        """Start the log viewer."""
        self._running = True
        self.load_files()

        if self.follow:
            self._follow_mode()
        else:
            self._interactive_mode()

    def _follow_mode(self):
        """Follow mode - continuously monitor files for changes."""
        while self._running and self.follow:
            if self._paused:
                time.sleep(0.1)
                continue

            for filepath in self.files:
                if not os.path.exists(filepath):
                    continue
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                        f.seek(self._file_positions.get(filepath, 0))
                        new_lines = f.readlines()
                        if new_lines:
                            self._file_positions[filepath] = f.tell()
                            for line in new_lines:
                                entry = self._parse_line(line.strip(), filepath)
                                if entry and self._apply_filters(entry):
                                    self.buffer.add(entry)
                                    self._notify_callbacks(entry)
                                    self.display.print_entry(self._apply_highlighting(entry))
                except Exception as e:
                    print(f"Error following {filepath}: {e}")
            time.sleep(0.1)

    def _interactive_mode(self):
        """Interactive mode for browsing logs."""
        entries = self.buffer.get_all()
        self.display.render(entries, self._apply_highlighting)

    def pause(self):
        """Pause following."""
        self._paused = True

    def resume(self):
        """Resume following."""
        self._paused = False

    def stop(self):
        """Stop the viewer."""
        self._running = False

    def add_bookmark(self, line_number: int):
        """Bookmark a line."""
        if line_number not in self._bookmarks:
            self._bookmarks.append(line_number)
            self._bookmarks.sort()

    def remove_bookmark(self, line_number: int):
        """Remove a bookmark."""
        if line_number in self._bookmarks:
            self._bookmarks.remove(line_number)

    def get_bookmarks(self) -> List[int]:
        """Get all bookmarks."""
        return self._bookmarks.copy()

    def export_filtered(self, filepath: str, entries: Optional[List[dict]] = None):
        """Export filtered entries to a file."""
        if entries is None:
            entries = self.buffer.get_all()
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                for entry in entries:
                    f.write(entry.get('raw', entry.get('line', '')) + '\n')
            return True
        except Exception as e:
            print(f"Export error: {e}")
            return False

    def search(self, pattern: str, case_sensitive: bool = False) -> List[dict]:
        """Search for entries matching a pattern."""
        results = []
        for entry in self.buffer.get_all():
            line = entry.get('raw', entry.get('line', ''))
            if not case_sensitive:
                if pattern.lower() in line.lower():
                    results.append(entry)
            else:
                if pattern in line:
                    results.append(entry)
        return results

    def get_stats(self) -> dict:
        """Get statistics about loaded logs."""
        entries = self.buffer.get_all()
        levels = {}
        for entry in entries:
            level = entry.get('level', 'UNKNOWN')
            levels[level] = levels.get(level, 0) + 1
        return {
            'total': len(entries),
            'levels': levels,
            'files': len(self.files),
            'bookmarks': len(self._bookmarks)
        }
