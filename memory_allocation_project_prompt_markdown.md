# Memory Allocation Project Using Segmentation — Full Project Specification

## Project Goal
Build a complete desktop application that simulates **Memory Allocation using Segmentation**.

The project must include:
- A modern and clean GUI.
- Full implementation of segmentation memory management.
- Allocation and deallocation operations.
- Support for both:
  - First Fit Allocation
  - Best Fit Allocation
- Real-time memory visualization.
- Runnable `.exe` desktop application.
- Source code with clean architecture and comments.
- Report screenshots export support.

---

# Required Technologies

## Programming Language
Use one of the following:
- C++ with Qt (preferred)
- C# Windows Forms / WPF
- JavaFX
- Python with PyQt5 or PySide6

## Important Requirement
The final project MUST generate:
- A standalone runnable `.exe` file.
- GUI desktop application.
- Source code files.

---

# Main Concept

Implement a memory allocation simulator using:

## Segmentation Technique
A process consists of multiple segments.
Each segment has:
- Segment Name
- Segment Size

Example:

Process P1:
- Code Segment → 50 KB
- Data Segment → 200 KB
- Stack Segment → 100 KB

The simulator must allocate each segment independently into memory holes.

---

# Functional Requirements

# 1. Total Memory Initialization

The application must allow the user to:
- Enter total memory size.
- Visualize memory initially.

Example:
- Total Memory = 1000 KB

---

# 2. Holes Initialization

The user must be able to add holes before allocation.

Each hole contains:
- Starting Address
- Hole Size

Example:

| Hole | Start Address | Size |
|------|---------------|------|
| H1 | 100 | 200 |
| H2 | 500 | 100 |

Requirements:
- Validate inputs.
- Prevent overlapping holes.
- Sort holes by starting address.
- Merge neighboring holes automatically.

---

# 3. Process Creation

The user must be able to add processes dynamically.

For each process:
- Enter Process Name.
- Enter Number of Segments.
- Enter Segment Name.
- Enter Segment Size.

Example:

Process P1:

| Segment | Size |
|---------|------|
| Code | 50 |
| Data | 200 |
| Stack | 100 |

Requirements:
- Dynamic number of segments.
- Input validation.
- Segment table generation.

---

# 4. Allocation Algorithms

Implement BOTH algorithms:

## First Fit
Allocate the segment into the first hole large enough.

## Best Fit
Allocate the segment into the smallest possible fitting hole.

The user must be able to choose the allocation strategy.

---

# 5. Allocation Rules

When allocating:
- Each segment is allocated independently.
- Update allocated partitions table.
- Update holes table.
- Reduce hole size after allocation.
- Remove hole if fully consumed.
- Memory visualization must update instantly.

If any segment of a process cannot fit:
- Show clear error message.
- Entire process allocation should fail.
- Rollback partial allocations.

Example Error:

"Process P2 cannot fit into memory."

---

# 6. Deallocation

The application must allow:
- Selecting a process.
- Deallocating all segments of that process.

Requirements:
- Convert freed segments into holes.
- Merge neighboring holes automatically.
- Update memory visualization.
- Update holes table.
- Update allocated partitions table.

---

# 7. Memory Visualization

The application MUST include a graphical memory representation.

## Visualization Requirements

Display memory vertically.

Each block should show:
- Segment Name
- Process Name
- Starting Address
- Ending Address
- Hole or Allocated state

Use different colors for:
- Allocated Segments
- Free Holes
- Reserved Memory

The memory layout must update after:
- Allocation
- Deallocation
- Initialization

---

# 8. Segment Table Display

Display a segment table for each process.

The table should contain:

| Segment | Base Address | Limit |
|----------|--------------|-------|
| Code | 100 | 50 |
| Data | 200 | 200 |

Requirements:
- Real-time updates.
- Show only allocated segments.

---

# 9. Allocated Partitions Table

Create a table for allocated partitions.

Columns:
- Process Name
- Segment Name
- Base Address
- Size

---

# 10. Free Holes Table

Create a table for free holes.

Columns:
- Hole Number
- Starting Address
- Size

Requirements:
- Automatically updated.
- Sorted by address.

---

# GUI Requirements

The GUI must be modern and user friendly.

## Required GUI Sections

### Left Panel
Controls:
- Total memory size input
- Add hole form
- Add process form
- Allocation method selector
- Allocate button
- Deallocate button

### Center Panel
Memory visualization area.

### Right Panel
Tables:
- Holes Table
- Allocated Partitions Table
- Segment Tables

---

# Advanced Features (Strongly Recommended)

Add the following features:

## Animations
- Smooth memory block rendering.
- Allocation/deallocation animations.

## Dark Mode
- Optional dark/light themes.

## Validation
- Invalid address checks.
- Negative number prevention.
- Overlap detection.

## Scrollable Memory View
For large memory sizes.

## Export Feature
- Export memory screenshot.
- Export report data.

## Statistics Panel
Display:
- Total Memory
- Used Memory
- Free Memory
- Fragmentation Percentage

---

# Data Structures

Use suitable OOP design.

## Suggested Classes

### Segment
Properties:
- name
- size
- baseAddress

### Process
Properties:
- processName
- list of segments

### Hole
Properties:
- startAddress
- size

### MemoryManager
Responsibilities:
- Allocation
- Deallocation
- Hole merging
- Memory visualization data
- Tables updating

---

# Allocation Logic

## First Fit Pseudocode

```text
for each segment:
    for each hole:
        if hole size >= segment size:
            allocate segment
            update hole
            break
```

## Best Fit Pseudocode

```text
for each segment:
    choose smallest fitting hole
    allocate segment
    update hole
```

---

# Hole Merging Logic

When deallocating:

```text
sort holes by address
merge adjacent holes
```

Example:

Before Merge:
- Hole 1: 100 → 50
- Hole 2: 150 → 100

After Merge:
- Hole: 100 → 150

---

# Memory Layout Rules

Reserved areas that are not holes should appear as:
- Reserved / Unused Memory.

Memory must always remain sorted by address.

---

# Required User Scenarios

## Scenario 1
Initialize memory and holes.

## Scenario 2
Allocate process using First Fit.

## Scenario 3
Allocate process using Best Fit.

## Scenario 4
Fail allocation due to insufficient space.

## Scenario 5
Deallocate process.

## Scenario 6
Merge adjacent holes.

---

# Error Handling

Handle all edge cases:

- Overlapping holes.
- Hole outside memory range.
- Invalid segment sizes.
- Duplicate process names.
- Allocation failure.
- Empty inputs.
- Negative values.
- Non-numeric values.

---

# Output Requirements

The final project output must include:

## 1. GUI Application
Fully working desktop application.

## 2. Runnable EXE File
Standalone executable.

## 3. Source Code
Organized and documented.

## 4. PDF Report
The report should include:
- Project description
- Algorithms explanation
- Screenshots
- Test cases
- Memory allocation examples
- Challenges and solutions

## 5. Drive Link
Upload executable to Google Drive.

---

# Suggested GUI Design

## Top Toolbar
- New Memory
- Add Hole
- Add Process
- Allocate
- Deallocate
- Reset

## Main Window

### Left Side
Forms and controls.

### Middle
Large vertical memory visualization.

### Right Side
Tables and process details.

---

# Visual Design Suggestions

Use:
- Rounded corners
- Modern buttons
- Consistent spacing
- Responsive layout
- Colored memory blocks
- Hover effects
- Scroll support

---

# Performance Requirements

The application should:
- Handle many processes.
- Update visualization instantly.
- Avoid crashes.
- Prevent memory leaks.

---

# Testing Requirements

Test the following:

- Full allocation.
- Partial allocation failure.
- Best fit correctness.
- First fit correctness.
- Hole merging.
- Large memory sizes.
- Consecutive deallocations.
- Consecutive allocations.

---

# Deliverables Checklist

The final submission must contain:

- Source code files.
- Runnable `.exe` application.
- PDF report.
- Screenshots.
- Google Drive executable link.
- README.md file.

---

# README.md Requirements

The generated project must include a professional README file containing:

- Project title
- Features
- Screenshots
- Installation steps
- Running instructions
- Allocation algorithms explanation
- Authors

---

# Important Notes

VERY IMPORTANT:
- Read every requirement carefully.
- Do NOT skip any feature.
- The GUI is mandatory.
- The executable file is mandatory.
- Memory visualization is mandatory.
- Both allocation algorithms are mandatory.
- Hole merging is mandatory.
- Tables updating is mandatory.
- The project must be polished and professional.

---

# Final Goal

Create a professional operating systems project that simulates memory allocation using segmentation with:

- Beautiful GUI
- Real-time visualization
- First Fit and Best Fit algorithms
- Allocation and deallocation
- Dynamic hole management
- Segment tables
- Runnable executable
- Clean architecture
- Professional report

