"""
MemoryBlock model class.
Represents a contiguous block in the memory layout for visualization.
A block can be a hole, an allocated segment, or reserved memory.
"""

from enum import Enum


class BlockType(Enum):
    """Types of memory blocks for visualization."""
    HOLE = "hole"
    ALLOCATED = "allocated"
    RESERVED = "reserved"


class MemoryBlock:
    """
    A contiguous block of memory used for building the
    visual memory layout. Each block has a type, address range,
    and optional label information.
    """

    def __init__(self, start_address: int, size: int, block_type: BlockType,
                 process_name: str = "", segment_name: str = ""):
        """
        Initialize a MemoryBlock.

        Args:
            start_address: Starting address of this block.
            size: Size of this block in KB.
            block_type: Type of memory block (HOLE, ALLOCATED, RESERVED).
            process_name: Name of the owning process (if allocated).
            segment_name: Name of the segment (if allocated).
        """
        self.start_address = start_address
        self.size = size
        self.block_type = block_type
        self.process_name = process_name
        self.segment_name = segment_name

    @property
    def end_address(self) -> int:
        """Return the ending address (exclusive) of this block."""
        return self.start_address + self.size

    @property
    def label(self) -> str:
        """Return a display label for this block."""
        if self.block_type == BlockType.HOLE:
            return "Free Hole"
        elif self.block_type == BlockType.ALLOCATED:
            return f"{self.process_name} — {self.segment_name}"
        else:
            return "Reserved"

    def __repr__(self) -> str:
        return (f"MemoryBlock({self.start_address}-{self.end_address}, "
                f"{self.block_type.value}, '{self.label}')")
