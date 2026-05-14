"""
Hole model class.
Represents a free memory hole (unallocated region) in memory.
"""


class Hole:
    """A free memory hole available for allocation."""

    def __init__(self, start_address: int, size: int):
        """
        Initialize a Hole.

        Args:
            start_address: Starting address of the hole.
            size: Size of the hole in KB.
        """
        self.start_address = start_address
        self.size = size

    @property
    def end_address(self) -> int:
        """Return the ending address (exclusive) of this hole."""
        return self.start_address + self.size

    def can_fit(self, segment_size: int) -> bool:
        """Check if a segment of given size can fit in this hole."""
        return self.size >= segment_size

    def __repr__(self) -> str:
        return (f"Hole(start={self.start_address}, size={self.size}, "
                f"end={self.end_address})")
