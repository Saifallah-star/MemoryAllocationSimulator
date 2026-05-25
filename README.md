#  Memory Allocation Simulator — Segmentation

A professional desktop application that simulates **Memory Allocation using Segmentation**, built for Operating Systems coursework.

##  Features

- **Segmentation-based memory management** with real-time visualization
- **Two allocation algorithms**: First Fit & Best Fit
- **Dynamic process creation** with configurable segments
- **Automatic hole merging** on deallocation
- **Rollback support** — if any segment fails, entire allocation is undone
- **Three-panel GUI**: Controls | Memory Map | Data Tables
- **Dark modern theme** with smooth, professional styling
- **Live statistics**: total/used/free memory, fragmentation percentage
- **Export screenshots** of the memory visualization
- **Complete input validation** and error handling

### Memory Visualization
Each memory block displays:
- Segment name and owning process
- Start and end addresses
- Block size in KB
- Color coding: purple/blue/green for processes, gray dashed for holes, dark for reserved

##  Technology Stack

| Component     | Technology          |
|---------------|---------------------|
| Language      | Python 3.10+        |
| GUI Framework | PySide6 (Qt 6)      |
| Packaging     | PyInstaller         |
| Architecture  | Clean OOP (MVC-like)|

##  Project Structure

```
memory assignment/
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── test_cases.py            # Automated test suite (10 tests)
├── build_exe.py             # Standalone EXE build script
├── README.md                # This file
├── models/                  # Data model classes
│   ├── __init__.py
│   ├── segment.py           # Segment (name, size, base address)
│   ├── process.py           # Process (name, list of segments)
│   ├── hole.py              # Hole (start address, size)
│   └── memory_block.py      # MemoryBlock + BlockType enum
├── core/                    # Business logic engine
│   ├── __init__.py
│   └── memory_manager.py    # MemoryManager (allocation, deallocation, merging)
└── gui/                     # GUI layer
    ├── __init__.py
    ├── styles.py            # Dark theme QSS stylesheet
    ├── memory_view.py       # Custom memory visualization widget
    └── main_window.py       # Main application window
```

##  Installation & Running

### Prerequisites
- Python 3.10 or newer
- pip package manager

### Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
python main.py

# 3. (Optional) Run tests
python test_cases.py
```

## Building Standalone EXE

```bash
# Generate a standalone executable
python build_exe.py
```

The executable will be created in the `dist/` folder. You can distribute it without requiring Python to be installed.

### Manual PyInstaller command
```bash
pyinstaller --onefile --windowed --name "MemoryAllocSimulator" main.py
```

## Allocation Algorithms

### First Fit
Scans holes **in address order** and allocates the segment to the **first hole** large enough to hold it.

- **Advantage**: Fast — stops at the first suitable hole.
- **Disadvantage**: Tends to fragment the beginning of memory.

### Best Fit
Scans **all holes** and selects the **smallest hole** that can fit the segment.

- **Advantage**: Minimizes wasted space per allocation.
- **Disadvantage**: Slower scan; can produce many tiny unusable holes.

### Rollback Mechanism
If a process has multiple segments and any segment cannot be allocated, the entire process allocation is **rolled back** — all partially allocated segments are freed and holes are restored to their pre-allocation state.


Run them: `python test_cases.py`

##  Authors

- Operating Systems Course — University Project

##  License

This project is for educational purposes.
