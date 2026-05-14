"""
Process model class.
Represents a process consisting of multiple segments.
"""

from typing import List
from models.segment import Segment


class Process:
    """A process composed of multiple memory segments."""

    def __init__(self, name: str, segments: List[Segment] = None):
        """
        Initialize a Process.

        Args:
            name: Process name (e.g., "P1", "Browser").
            segments: List of Segment objects belonging to this process.
        """
        self.name = name
        self.segments: List[Segment] = segments if segments is not None else []

    def add_segment(self, segment: Segment) -> None:
        """Add a segment to this process."""
        self.segments.append(segment)

    @property
    def is_allocated(self) -> bool:
        """Check if all segments of this process are allocated."""
        return len(self.segments) > 0 and all(s.is_allocated for s in self.segments)

    @property
    def total_size(self) -> int:
        """Return total size of all segments."""
        return sum(s.size for s in self.segments)

    def deallocate_all(self) -> None:
        """Deallocate all segments of this process."""
        for segment in self.segments:
            segment.deallocate()

    def __repr__(self) -> str:
        return (f"Process(name='{self.name}', segments={len(self.segments)}, "
                f"total_size={self.total_size})")
