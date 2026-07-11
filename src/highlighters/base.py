"""Base highlighter interface."""
from abc import ABC, abstractmethod
from typing import Dict, Tuple


class BaseHighlighter(ABC):
    """Abstract base class for syntax highlighting."""

    # ANSI color codes
    COLORS = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m',
        'gray': '\033[90m',
        'reset': '\033[0m',
        'bold': '\033[1m',
        'underline': '\033[4m',
    }

    @abstractmethod
    def highlight(self, line: str, entry: dict = None) -> str:
        """Apply highlighting to a log line.
        
        Args:
            line: The log line to highlight
            entry: Optional parsed entry dict for context
            
        Returns:
            Highlighted line with ANSI codes
        """
        pass

    def _colorize(self, text: str, color: str) -> str:
        """Wrap text with color ANSI codes."""
        color_code = self.COLORS.get(color, '')
        reset_code = self.COLORS['reset']
        if color_code:
            return f"{color_code}{text}{reset_code}"
        return text
