"""Base filter interface."""
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseFilter(ABC):
    """Abstract base class for log filters."""

    @abstractmethod
    def matches(self, entry: dict) -> bool:
        """Check if a log entry matches this filter.
        
        Args:
            entry: Parsed log entry dict
            
        Returns:
            True if entry matches filter criteria
        """
        pass

    def __and__(self, other: 'BaseFilter') -> 'CompositeFilter':
        """Combine filters with AND logic."""
        return CompositeFilter(self, other, logic='AND')

    def __or__(self, other: 'BaseFilter') -> 'CompositeFilter':
        """Combine filters with OR logic."""
        return CompositeFilter(self, other, logic='OR')

    def __invert__(self) -> 'NegateFilter':
        """Negate this filter."""
        return NegateFilter(self)


class CompositeFilter(BaseFilter):
    """Combine multiple filters with AND/OR logic."""

    def __init__(self, filter_a: BaseFilter, filter_b: BaseFilter, logic: str = 'AND'):
        self.filter_a = filter_a
        self.filter_b = filter_b
        self.logic = logic.upper()

    def matches(self, entry: dict) -> bool:
        if self.logic == 'AND':
            return self.filter_a.matches(entry) and self.filter_b.matches(entry)
        else:
            return self.filter_a.matches(entry) or self.filter_b.matches(entry)


class NegateFilter(BaseFilter):
    """Negate a filter's result."""

    def __init__(self, filter_obj: BaseFilter):
        self.filter_obj = filter_obj

    def matches(self, entry: dict) -> bool:
        return not self.filter_obj.matches(entry)
