"""
test_cases.py — Automated test cases for the Memory Allocation Simulator.

Run with:  python test_cases.py
"""

from core.memory_manager import MemoryManager, AllocationStrategy
from models.process import Process
from models.segment import Segment


def test_initialization():
    """Test 1: Memory initialization."""
    print("=" * 60)
    print("TEST 1: Memory Initialization")
    mm = MemoryManager()
    mm.initialize_memory(1000)
    assert mm.total_memory == 1000
    assert mm.is_initialized
    stats = mm.get_statistics()
    assert stats["total"] == 1000
    assert stats["reserved"] == 1000
    print("  ✓ Memory initialized to 1000 KB")
    print("  ✓ All memory is reserved (no holes, no processes)")
    print("  PASSED\n")


def test_add_holes():
    """Test 2: Adding holes and validation."""
    print("=" * 60)
    print("TEST 2: Adding Holes")
    mm = MemoryManager()
    mm.initialize_memory(1000)

    mm.add_hole(100, 200)
    mm.add_hole(500, 100)
    assert len(mm.holes) == 2
    print("  ✓ Two non-overlapping holes added")

    # Test overlap detection
    try:
        mm.add_hole(150, 100)
        assert False, "Should have raised ValueError"
    except ValueError:
        print("  ✓ Overlapping hole correctly rejected")

    # Test out-of-bounds
    try:
        mm.add_hole(950, 100)
        assert False, "Should have raised ValueError"
    except ValueError:
        print("  ✓ Out-of-bounds hole correctly rejected")

    print("  PASSED\n")


def test_hole_merging():
    """Test 3: Automatic hole merging."""
    print("=" * 60)
    print("TEST 3: Hole Merging")
    mm = MemoryManager()
    mm.initialize_memory(1000)

    mm.add_hole(100, 50)   # 100–150
    mm.add_hole(150, 100)  # 150–250 (adjacent to first)
    assert len(mm.holes) == 1, f"Expected 1 merged hole, got {len(mm.holes)}"
    assert mm.holes[0].start_address == 100
    assert mm.holes[0].size == 150
    print("  ✓ Adjacent holes merged: [100,50] + [150,100] → [100,150]")
    print("  PASSED\n")


def test_first_fit_allocation():
    """Test 4: First Fit allocation."""
    print("=" * 60)
    print("TEST 4: First Fit Allocation")
    mm = MemoryManager()
    mm.initialize_memory(1000)
    mm.add_hole(100, 200)  # H1: 100–300
    mm.add_hole(500, 150)  # H2: 500–650

    p = Process("P1", [
        Segment("Code", 50),
        Segment("Data", 100),
    ])
    mm.add_process(p)
    ok, msg = mm.allocate_process("P1", AllocationStrategy.FIRST_FIT)
    assert ok, msg
    print(f"  ✓ {msg}")

    # Code should go to H1 start (100), Data to 150
    assert p.segments[0].base_address == 100
    assert p.segments[1].base_address == 150
    print(f"  ✓ Code@100, Data@150 (both in first hole)")

    # Remaining hole should be [250, 50] and [500, 150]
    assert len(mm.holes) == 2
    assert mm.holes[0].start_address == 250
    assert mm.holes[0].size == 50
    print(f"  ✓ Remaining holes: {mm.holes}")
    print("  PASSED\n")


def test_best_fit_allocation():
    """Test 5: Best Fit allocation."""
    print("=" * 60)
    print("TEST 5: Best Fit Allocation")
    mm = MemoryManager()
    mm.initialize_memory(1000)
    mm.add_hole(0, 300)    # H1: 0–300 (large)
    mm.add_hole(400, 100)  # H2: 400–500 (small)
    mm.add_hole(600, 200)  # H3: 600–800 (medium)

    p = Process("P1", [Segment("Code", 80)])
    mm.add_process(p)
    ok, msg = mm.allocate_process("P1", AllocationStrategy.BEST_FIT)
    assert ok, msg

    # Best fit should pick H2 (size 100, smallest that fits 80)
    assert p.segments[0].base_address == 400
    print(f"  ✓ Best Fit picked hole at 400 (size 100) for segment of 80")
    print(f"  ✓ {msg}")
    print("  PASSED\n")


def test_allocation_failure_and_rollback():
    """Test 6: Allocation failure with rollback."""
    print("=" * 60)
    print("TEST 6: Allocation Failure + Rollback")
    mm = MemoryManager()
    mm.initialize_memory(1000)
    mm.add_hole(100, 50)   # Only 50 KB available

    p = Process("P1", [
        Segment("Code", 30),   # Fits
        Segment("Data", 200),  # Won't fit
    ])
    mm.add_process(p)
    ok, msg = mm.allocate_process("P1", AllocationStrategy.FIRST_FIT)
    assert not ok
    print(f"  ✓ Allocation failed: {msg}")

    # Rollback: segments should not be allocated
    assert not p.segments[0].is_allocated
    assert not p.segments[1].is_allocated
    print("  ✓ Partial allocation rolled back")

    # Holes should be unchanged
    assert len(mm.holes) == 1
    assert mm.holes[0].size == 50
    print("  ✓ Holes restored to pre-allocation state")
    print("  PASSED\n")


def test_deallocation_and_merge():
    """Test 7: Deallocation + hole merging."""
    print("=" * 60)
    print("TEST 7: Deallocation + Hole Merging")
    mm = MemoryManager()
    mm.initialize_memory(1000)
    mm.add_hole(0, 1000)  # Entire memory is free

    p = Process("P1", [
        Segment("Code", 100),
        Segment("Data", 200),
    ])
    mm.add_process(p)
    mm.allocate_process("P1", AllocationStrategy.FIRST_FIT)
    assert p.is_allocated
    print(f"  ✓ P1 allocated: Code@0, Data@100")

    # Now deallocate
    ok, msg = mm.deallocate_process("P1")
    assert ok
    print(f"  ✓ {msg}")

    # After deallocation, freed segments should merge back into one hole
    assert len(mm.holes) == 1
    assert mm.holes[0].start_address == 0
    assert mm.holes[0].size == 1000
    print("  ✓ All holes merged back to [0, 1000]")
    print("  PASSED\n")


def test_duplicate_process():
    """Test 8: Duplicate process name prevention."""
    print("=" * 60)
    print("TEST 8: Duplicate Process Name")
    mm = MemoryManager()
    mm.initialize_memory(1000)

    mm.add_process(Process("P1", [Segment("Code", 50)]))
    try:
        mm.add_process(Process("P1", [Segment("Data", 100)]))
        assert False, "Should have raised ValueError"
    except ValueError:
        print("  ✓ Duplicate process name 'P1' correctly rejected")
    print("  PASSED\n")


def test_memory_layout():
    """Test 9: Memory layout generation for visualization."""
    print("=" * 60)
    print("TEST 9: Memory Layout Generation")
    mm = MemoryManager()
    mm.initialize_memory(1000)
    mm.add_hole(100, 200)
    mm.add_hole(500, 100)

    layout = mm.get_memory_layout()
    print(f"  Layout blocks: {len(layout)}")
    for b in layout:
        print(f"    {b}")

    # Expected: RESERVED[0-100], HOLE[100-300], RESERVED[300-500],
    #           HOLE[500-600], RESERVED[600-1000]
    assert len(layout) == 5
    print("  ✓ Layout correctly shows reserved + hole regions")
    print("  PASSED\n")


def test_statistics():
    """Test 10: Statistics calculation."""
    print("=" * 60)
    print("TEST 10: Statistics")
    mm = MemoryManager()
    mm.initialize_memory(1000)
    mm.add_hole(0, 500)
    mm.add_hole(700, 300)

    p = Process("P1", [Segment("Code", 200)])
    mm.add_process(p)
    mm.allocate_process("P1", AllocationStrategy.FIRST_FIT)

    stats = mm.get_statistics()
    print(f"  Total:    {stats['total']} KB")
    print(f"  Used:     {stats['used']} KB")
    print(f"  Free:     {stats['free']} KB")
    print(f"  Reserved: {stats['reserved']} KB")
    print(f"  Fragmentation: {stats['fragmentation']}%")

    assert stats["total"] == 1000
    assert stats["used"] == 200
    assert stats["free"] == 600  # 300 + 300
    assert stats["reserved"] == 200  # [500-700]
    print("  ✓ Statistics correct")
    print("  PASSED\n")


def main():
    """Run all test cases."""
    print("\n" + "═" * 60)
    print("  MEMORY ALLOCATION SIMULATOR — TEST SUITE")
    print("═" * 60 + "\n")

    test_initialization()
    test_add_holes()
    test_hole_merging()
    test_first_fit_allocation()
    test_best_fit_allocation()
    test_allocation_failure_and_rollback()
    test_deallocation_and_merge()
    test_duplicate_process()
    test_memory_layout()
    test_statistics()

    print("═" * 60)
    print("  ALL 10 TESTS PASSED ✓")
    print("═" * 60 + "\n")


if __name__ == "__main__":
    main()
