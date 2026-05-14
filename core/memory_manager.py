"""
MemoryManager — the core allocation engine.

Responsibilities:
  - Initialize total memory and holes.
  - Allocate processes using First Fit or Best Fit.
  - Deallocate processes.
  - Merge neighboring holes automatically.
  - Build the memory layout for visualization.
  - Provide data for segment tables, allocated partitions, and holes tables.
"""

from enum import Enum
from typing import List, Optional, Tuple, Dict
from copy import deepcopy

from models.segment import Segment
from models.process import Process
from models.hole import Hole
from models.memory_block import MemoryBlock, BlockType


class AllocationStrategy(Enum):
    """Available allocation algorithms."""
    FIRST_FIT = "First Fit"
    BEST_FIT = "Best Fit"


class MemoryManager:
    """
    Core memory management engine.
    Handles allocation, deallocation, hole management, and provides
    data for the GUI tables and visualization.
    """

    def __init__(self):
        """Initialize an empty memory manager."""
        self.total_memory: int = 0
        self.holes: List[Hole] = []
        self.processes: Dict[str, Process] = {}  # name → Process
        self._initialized = False

    # ─── Initialization ─────────────────────────────────────────────────

    def initialize_memory(self, total_size: int) -> None:
        """
        Set the total memory size and reset all state.

        Args:
            total_size: Total memory in KB (must be > 0).

        Raises:
            ValueError: If total_size is not positive.
        """
        if total_size <= 0:
            raise ValueError("Total memory size must be a positive integer.")
        self.total_memory = total_size
        self.holes.clear()
        self.processes.clear()
        self._initialized = True

    @property
    def is_initialized(self) -> bool:
        """Return whether the memory has been initialized."""
        return self._initialized

    # ─── Hole Management ────────────────────────────────────────────────

    def add_hole(self, start_address: int, size: int) -> None:
        """
        Add a free hole to memory.

        Validates that the hole is within bounds, non-overlapping, and
        merges with neighbours automatically.

        Args:
            start_address: Start address of the hole.
            size: Size of the hole in KB.

        Raises:
            ValueError: On invalid input, out-of-bounds, or overlap.
        """
        self._check_initialized()
        if start_address < 0:
            raise ValueError("Starting address cannot be negative.")
        if size <= 0:
            raise ValueError("Hole size must be a positive integer.")
        if start_address + size > self.total_memory:
            raise ValueError(
                f"Hole exceeds memory bounds. "
                f"End address ({start_address + size}) > "
                f"Total memory ({self.total_memory})."
            )

        # Check overlap with existing holes
        for hole in self.holes:
            if self._ranges_overlap(start_address, size,
                                    hole.start_address, hole.size):
                raise ValueError(
                    f"New hole [{start_address}, {start_address + size}) "
                    f"overlaps with existing hole "
                    f"[{hole.start_address}, {hole.end_address})."
                )

        # Check overlap with allocated segments
        for process in self.processes.values():
            for seg in process.segments:
                if seg.is_allocated:
                    if self._ranges_overlap(start_address, size,
                                            seg.base_address, seg.size):
                        raise ValueError(
                            f"New hole [{start_address}, {start_address + size}) "
                            f"overlaps with allocated segment "
                            f"'{seg.name}' of process '{process.name}'."
                        )

        self.holes.append(Hole(start_address, size))
        self._sort_holes()
        self._merge_holes()

    def _sort_holes(self) -> None:
        """Sort holes by starting address."""
        self.holes.sort(key=lambda h: h.start_address)

    def _merge_holes(self) -> None:
        """Merge all adjacent or overlapping holes."""
        if len(self.holes) <= 1:
            return

        self._sort_holes()
        merged: List[Hole] = [self.holes[0]]
        for hole in self.holes[1:]:
            last = merged[-1]
            if hole.start_address <= last.end_address:
                # Merge: extend the last hole
                new_end = max(last.end_address, hole.end_address)
                last.size = new_end - last.start_address
            else:
                merged.append(hole)
        self.holes = merged

    @staticmethod
    def _ranges_overlap(start1: int, size1: int,
                        start2: int, size2: int) -> bool:
        """Check if two memory ranges overlap."""
        end1 = start1 + size1
        end2 = start2 + size2
        return start1 < end2 and start2 < end1

    # ─── Process & Segment Management ───────────────────────────────────

    def add_process(self, process: Process) -> None:
        """
        Register a process (does NOT allocate it yet).

        Args:
            process: Process object to register.

        Raises:
            ValueError: If process name is duplicate or invalid.
        """
        self._check_initialized()
        if not process.name.strip():
            raise ValueError("Process name cannot be empty.")
        if process.name in self.processes:
            raise ValueError(f"Process '{process.name}' already exists.")
        if len(process.segments) == 0:
            raise ValueError("Process must have at least one segment.")
        for seg in process.segments:
            if seg.size <= 0:
                raise ValueError(
                    f"Segment '{seg.name}' has invalid size ({seg.size}). "
                    "Size must be positive."
                )
        self.processes[process.name] = process

    # ─── Allocation ─────────────────────────────────────────────────────

    def allocate_process(self, process_name: str,
                         strategy: AllocationStrategy) -> Tuple[bool, str]:
        """
        Allocate all segments of a process using the specified strategy.

        If any segment cannot fit, the entire allocation is rolled back.

        Args:
            process_name: Name of the process to allocate.
            strategy: FIRST_FIT or BEST_FIT.

        Returns:
            (success, message) tuple.
        """
        self._check_initialized()
        if process_name not in self.processes:
            return False, f"Process '{process_name}' not found."

        process = self.processes[process_name]
        if process.is_allocated:
            return False, f"Process '{process_name}' is already allocated."

        # Save holes state for rollback
        holes_backup = deepcopy(self.holes)

        allocations: List[Tuple[Segment, int]] = []  # (segment, hole_index)
        success = True
        fail_segment = ""

        for segment in process.segments:
            hole_index = self._find_hole(segment.size, strategy)
            if hole_index == -1:
                success = False
                fail_segment = segment.name
                break

            # Perform allocation
            hole = self.holes[hole_index]
            segment.allocate(hole.start_address)
            allocations.append((segment, hole_index))

            # Update hole
            if hole.size == segment.size:
                self.holes.pop(hole_index)
            else:
                hole.start_address += segment.size
                hole.size -= segment.size

        if not success:
            # Rollback all partial allocations
            for seg, _ in allocations:
                seg.deallocate()
            self.holes = holes_backup
            return False, (
                f"Process '{process_name}' cannot fit into memory. "
                f"Segment '{fail_segment}' has no suitable hole."
            )

        return True, (
            f"Process '{process_name}' allocated successfully "
            f"using {strategy.value}."
        )

    def _find_hole(self, size: int,
                   strategy: AllocationStrategy) -> int:
        """
        Find a hole index for a segment of the given size.

        Args:
            size: Required segment size.
            strategy: Allocation strategy.

        Returns:
            Index of the chosen hole, or -1 if none fits.
        """
        if strategy == AllocationStrategy.FIRST_FIT:
            return self._first_fit(size)
        else:
            return self._best_fit(size)

    def _first_fit(self, size: int) -> int:
        """First Fit: return index of first hole that fits."""
        for i, hole in enumerate(self.holes):
            if hole.can_fit(size):
                return i
        return -1

    def _best_fit(self, size: int) -> int:
        """Best Fit: return index of smallest hole that fits."""
        best_index = -1
        best_diff = float('inf')
        for i, hole in enumerate(self.holes):
            if hole.can_fit(size):
                diff = hole.size - size
                if diff < best_diff:
                    best_diff = diff
                    best_index = i
        return best_index

    # ─── Deallocation ───────────────────────────────────────────────────

    def deallocate_process(self, process_name: str) -> Tuple[bool, str]:
        """
        Deallocate all segments of a process and convert them to holes.
        Adjacent holes are merged automatically.

        Args:
            process_name: Name of the process to deallocate.

        Returns:
            (success, message) tuple.
        """
        self._check_initialized()
        if process_name not in self.processes:
            return False, f"Process '{process_name}' not found."

        process = self.processes[process_name]
        if not process.is_allocated:
            return False, f"Process '{process_name}' is not currently allocated."

        # Convert each allocated segment into a hole
        for segment in process.segments:
            if segment.is_allocated:
                self.holes.append(
                    Hole(segment.base_address, segment.size)
                )
                segment.deallocate()

        # Sort and merge holes
        self._sort_holes()
        self._merge_holes()

        return True, (
            f"Process '{process_name}' deallocated successfully. "
            f"Holes merged; process remains registered."
        )

    # ─── Memory Layout for Visualization ────────────────────────────────

    def get_memory_layout(self) -> List[MemoryBlock]:
        """
        Build a sorted list of MemoryBlocks covering the entire memory.
        Gaps between holes/segments are filled with RESERVED blocks.

        Returns:
            Sorted list of MemoryBlock objects.
        """
        if not self._initialized:
            return []

        # Collect all known regions
        regions: List[MemoryBlock] = []

        # Add holes
        for hole in self.holes:
            regions.append(MemoryBlock(
                hole.start_address, hole.size, BlockType.HOLE
            ))

        # Add allocated segments
        for process in self.processes.values():
            for seg in process.segments:
                if seg.is_allocated:
                    regions.append(MemoryBlock(
                        seg.base_address, seg.size, BlockType.ALLOCATED,
                        process.name, seg.name
                    ))

        # Sort by start address
        regions.sort(key=lambda b: b.start_address)

        # Fill gaps with RESERVED blocks
        full_layout: List[MemoryBlock] = []
        current = 0

        for block in regions:
            if block.start_address > current:
                full_layout.append(MemoryBlock(
                    current, block.start_address - current, BlockType.RESERVED
                ))
            full_layout.append(block)
            current = block.end_address

        # Trailing reserved space
        if current < self.total_memory:
            full_layout.append(MemoryBlock(
                current, self.total_memory - current, BlockType.RESERVED
            ))

        return full_layout

    # ─── Table Data ─────────────────────────────────────────────────────

    def get_holes_table_data(self) -> List[dict]:
        """Return data for the Free Holes table."""
        data = []
        for i, hole in enumerate(self.holes):
            data.append({
                "hole_number": i + 1,
                "start_address": hole.start_address,
                "size": hole.size,
                "end_address": hole.end_address,
            })
        return data

    def get_allocated_partitions_data(self) -> List[dict]:
        """Return data for the Allocated Partitions table."""
        data = []
        for process in self.processes.values():
            for seg in process.segments:
                if seg.is_allocated:
                    data.append({
                        "process_name": process.name,
                        "segment_name": seg.name,
                        "base_address": seg.base_address,
                        "size": seg.size,
                        "end_address": seg.end_address,
                    })
        data.sort(key=lambda d: d["base_address"])
        return data

    def get_segment_table_data(self, process_name: str) -> List[dict]:
        """Return data for a specific process's segment table."""
        if process_name not in self.processes:
            return []
        process = self.processes[process_name]
        data = []
        for seg in process.segments:
            data.append({
                "segment_name": seg.name,
                "base_address": seg.base_address if seg.is_allocated else "N/A",
                "limit": seg.size,
                "allocated": seg.is_allocated,
            })
        return data

    def get_all_segment_tables(self) -> Dict[str, List[dict]]:
        """Return segment tables for all processes."""
        result = {}
        for name in self.processes:
            result[name] = self.get_segment_table_data(name)
        return result

    # ─── Statistics ─────────────────────────────────────────────────────

    def get_statistics(self) -> dict:
        """Return memory usage statistics."""
        if not self._initialized:
            return {
                "total": 0, "used": 0, "free": 0,
                "reserved": 0, "fragmentation": 0.0,
                "num_holes": 0, "num_processes": 0,
            }

        total_free = sum(h.size for h in self.holes)
        total_allocated = sum(
            seg.size
            for p in self.processes.values()
            for seg in p.segments
            if seg.is_allocated
        )
        total_reserved = self.total_memory - total_free - total_allocated

        # External fragmentation: 1 - (largest_hole / total_free)
        if total_free > 0 and len(self.holes) > 1:
            largest_hole = max(h.size for h in self.holes)
            fragmentation = (1.0 - largest_hole / total_free) * 100
        else:
            fragmentation = 0.0

        return {
            "total": self.total_memory,
            "used": total_allocated,
            "free": total_free,
            "reserved": total_reserved,
            "fragmentation": round(fragmentation, 2),
            "num_holes": len(self.holes),
            "num_processes": len(self.processes),
        }

    def get_allocated_process_names(self) -> List[str]:
        """Return names of currently allocated processes."""
        return [
            name for name, proc in self.processes.items()
            if proc.is_allocated
        ]

    # ─── Reset ──────────────────────────────────────────────────────────

    def reset(self) -> None:
        """Reset the memory manager to initial state."""
        self.total_memory = 0
        self.holes.clear()
        self.processes.clear()
        self._initialized = False

    # ─── Helpers ────────────────────────────────────────────────────────

    def _check_initialized(self) -> None:
        """Raise an error if memory has not been initialized."""
        if not self._initialized:
            raise RuntimeError(
                "Memory has not been initialized. "
                "Please set total memory size first."
            )
