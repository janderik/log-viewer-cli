"""Terminal display rendering for log viewer."""
import sys
from typing import List, Optional


class Display:
    """Handles terminal rendering and display."""

    THEMES = {
        'default': {
            'ERROR': '\033[91m',
            'WARN': '\033[93m',
            'INFO': '\033[92m',
            'DEBUG': '\033[90m',
            'RESET': '\033[0m',
            'BOLD': '\033[1m',
            'TIMESTAMP': '\033[36m',
            'SOURCE': '\033[35m',
        },
        'monokai': {
            'ERROR': '\033[38;5;197m',
            'WARN': '\033[38;5;214m',
            'INFO': '\033[38;5;114m',
            'DEBUG': '\033[38;5;243m',
            'RESET': '\033[0m',
            'BOLD': '\033[1m',
            'TIMESTAMP': '\033[38;5;81m',
            'SOURCE': '\033[38;5;141m',
        },
        'solarized': {
            'ERROR': '\033[38;5;160m',
            'WARN': '\033[38;5;3m',
            'INFO': '\033[38;5;12m',
            'DEBUG': '\033[38;5;8m',
            'RESET': '\033[0m',
            'BOLD': '\033[1m',
            'TIMESTAMP': '\033[38;5;6m',
            'SOURCE': '\033[38;5;5m',
        },
        'light': {
            'ERROR': '\033[31m',
            'WARN': '\033[33m',
            'INFO': '\033[34m',
            'DEBUG': '\033[37m',
            'RESET': '\033[0m',
            'BOLD': '\033[1m',
            'TIMESTAMP': '\033[36m',
            'SOURCE': '\033[35m',
        }
    }

    def __init__(self, theme: str = "default"):
        self.theme = theme
        self.colors = self.THEMES.get(theme, self.THEMES['default'])
        self._visible_start = 0
        self._visible_lines = self._get_terminal_height()

    def _get_terminal_height(self) -> int:
        """Get terminal height."""
        try:
            return 40
        except Exception:
            return 40

    def _colorize(self, text: str, color: str) -> str:
        """Apply color to text."""
        code = self.colors.get(color, '')
        reset = self.colors.get('RESET', '')
        if code:
            return f"{code}{text}{reset}"
        return text

    def print_entry(self, line: str):
        """Print a single log entry."""
        print(line)
        sys.stdout.flush()

    def render(self, entries: List[dict], highlight_func=None):
        """Render a list of log entries."""
        for i, entry in enumerate(entries):
            raw = entry.get('raw', entry.get('line', ''))
            if highlight_func:
                line = highlight_func(entry)
            else:
                line = self._colorize_entry(entry)
            print(f"{i+1:5} {line}")
        sys.stdout.flush()

    def _colorize_entry(self, entry: dict) -> str:
        """Colorize a log entry based on level."""
        raw = entry.get('raw', entry.get('line', ''))
        level = entry.get('level', 'UNKNOWN')
        color = level.upper() if level.upper() in self.colors else 'INFO'
        return self._colorize(raw, color)

    def clear(self):
        """Clear the terminal."""
        print("\033[2J\033[H", end='')
        sys.stdout.flush()

    def set_theme(self, theme: str):
        """Change the color theme."""
        if theme in self.THEMES:
            self.theme = theme
            self.colors = self.THEMES[theme]

    def list_themes(self) -> List[str]:
        """List available themes."""
        return list(self.THEMES.keys())

    def show_status(self, stats: dict):
        """Display status bar."""
        total = stats.get('total', 0)
        files = stats.get('files', 0)
        levels = stats.get('levels', {})
        status = f"Total: {total} | Files: {files}"
        if levels:
            parts = [f"{k}: {v}" for k, v in levels.items()]
            status += f" | {', '.join(parts)}"
        print(f"\033[7m{status}\033[0m")
        sys.stdout.flush()

    def show_search_results(self, results: List[dict], query: str):
        """Display search results."""
        print(f"\nFound {len(results)} matches for '{query}':")
        for i, entry in enumerate(results[:50]):
            raw = entry.get('raw', entry.get('line', ''))
            print(f"  {i+1}. {raw[:100]}")
        if len(results) > 50:
            print(f"  ... and {len(results)-50} more")
