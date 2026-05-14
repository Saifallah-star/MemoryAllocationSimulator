"""
Segment model class.
Represents a single segment within a process (e.g., Code, Data, Stack).
"""


class Segment:
    """A memory segment belonging to a process."""

    def __init__(self, name: str, size: int, base_address: int = -1):
        """
        Initialize a Segment.

        Args:
            name: Segment name (e.g., "Code", "Data", "Stack").
            size: Size of the segment in KB.
            base_address: Starting address in memory (-1 if not yet allocated).
        """
        self.name = name
        self.size = size
        self.base_address = base_address

    @property
    def is_allocated(self) -> bool:
        """Check if this segment has been allocated in memory."""
        return self.base_address >= 0

    @property
    def end_address(self) -> int:
        """Return the ending address of this segment."""
        if not self.is_allocated:
            return -1
        return self.base_address + self.size

    @property
    def limit(self) -> int:
        """Return the limit (size) of this segment."""
        return self.size

    def allocate(self, base_address: int) -> None:
        """Assign a base address to this segment."""
        self.base_address = base_address

    def deallocate(self) -> None:
        """Free this segment from memory."""
        self.base_address = -1

    def __repr__(self) -> str:
        status = f"base={self.base_address}" if self.is_allocated else "unallocated"
        return f"Segment(name='{self.name}', size={self.size}, {status})"
