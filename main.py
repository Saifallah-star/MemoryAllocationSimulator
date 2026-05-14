"""
Memory Allocation Simulator — Entry Point
==========================================
A desktop application that simulates memory allocation
using segmentation with First Fit and Best Fit algorithms.

Run:  python main.py
"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

from gui.main_window import MainWindow
from gui.styles import DARK_STYLESHEET


def main():
    """Launch the Memory Allocation Simulator application."""
    app = QApplication(sys.argv)

    # Apply dark theme stylesheet
    app.setStyleSheet(DARK_STYLESHEET)

    # Set application-wide font
    font = QFont("Segoe UI", 13)
    app.setFont(font)

    # Application metadata
    app.setApplicationName("Memory Allocation Simulator")
    app.setOrganizationName("OS Course Project")
    app.setApplicationVersion("1.0.0")

    # Create and show the main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()


# ./venv/bin/python3 main.py