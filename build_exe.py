"""
build_exe.py — Build a standalone executable using PyInstaller.

Usage:
    python build_exe.py

Output:
    dist/MemoryAllocSimulator  (or .exe on Windows)
"""

import subprocess
import sys
import os


def build():
    """Build the standalone executable."""
    print("=" * 60)
    print("  Building Memory Allocation Simulator — Standalone EXE")
    print("=" * 60)

    # Ensure PyInstaller is installed
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("\n[!] PyInstaller not found. Installing...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "pyinstaller"]
        )

    # Build command
    project_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(project_dir, "main.py")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "MemoryAllocSimulator",
        "--clean",
        "--noconfirm",
        # Include package directories
        "--add-data", f"{os.path.join(project_dir, 'models')}{os.pathsep}models",
        "--add-data", f"{os.path.join(project_dir, 'core')}{os.pathsep}core",
        "--add-data", f"{os.path.join(project_dir, 'gui')}{os.pathsep}gui",
        # Hidden imports for PySide6
        "--hidden-import", "PySide6.QtWidgets",
        "--hidden-import", "PySide6.QtCore",
        "--hidden-import", "PySide6.QtGui",
        main_script,
    ]

    print(f"\nRunning: {' '.join(cmd)}\n")
    result = subprocess.run(cmd, cwd=project_dir)

    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("  ✓ Build successful!")
        print(f"  Executable location: dist/MemoryAllocSimulator")
        print("=" * 60)
    else:
        print("\n[✗] Build failed. Check the output above for errors.")
        sys.exit(1)


if __name__ == "__main__":
    build()
