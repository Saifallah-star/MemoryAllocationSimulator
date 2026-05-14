"""
Application-wide stylesheet for the dark modern theme.
Provides a consistent, polished look across all widgets.
"""

DARK_STYLESHEET = """
/* ── Global ───────────────────────────────────────────────── */
QWidget {
    background-color: #1a1b2e;
    color: #e0e0e8;
    font-family: "Segoe UI", "Inter", "Roboto", "Arial", sans-serif;
    font-size: 13px;
}

/* ── Main Window ──────────────────────────────────────────── */
QMainWindow {
    background-color: #1a1b2e;
}

/* ── Group Boxes (panel cards) ────────────────────────────── */
QGroupBox {
    background-color: #222342;
    border: 1px solid #3a3b5c;
    border-radius: 10px;
    margin-top: 14px;
    padding: 16px 10px 10px 10px;
    font-weight: 600;
    font-size: 14px;
    color: #b8b9d4;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 12px;
    color: #a78bfa;
    font-size: 13px;
    font-weight: 700;
}

/* ── Labels ───────────────────────────────────────────────── */
QLabel {
    color: #c4c5e0;
    font-size: 13px;
    background: transparent;
}

/* ── Line Edits ───────────────────────────────────────────── */
QLineEdit {
    background-color: #2a2b4a;
    border: 1px solid #4a4b6e;
    border-radius: 6px;
    padding: 7px 10px;
    color: #e0e0e8;
    font-size: 13px;
    selection-background-color: #7c3aed;
}
QLineEdit:focus {
    border: 1.5px solid #7c3aed;
}
QLineEdit:hover {
    border: 1px solid #6d5dfc;
}

/* ── Spin Boxes ───────────────────────────────────────────── */
QSpinBox {
    background-color: #2a2b4a;
    border: 1px solid #4a4b6e;
    border-radius: 6px;
    padding: 6px 10px;
    color: #e0e0e8;
    font-size: 13px;
}
QSpinBox:focus {
    border: 1.5px solid #7c3aed;
}
QSpinBox::up-button, QSpinBox::down-button {
    background-color: #3a3b5c;
    border: none;
    width: 20px;
    border-radius: 3px;
}
QSpinBox::up-button:hover, QSpinBox::down-button:hover {
    background-color: #7c3aed;
}

/* ── Combo Boxes ──────────────────────────────────────────── */
QComboBox {
    background-color: #2a2b4a;
    border: 1px solid #4a4b6e;
    border-radius: 6px;
    padding: 7px 10px;
    color: #e0e0e8;
    font-size: 13px;
    min-width: 120px;
}
QComboBox:hover {
    border: 1px solid #6d5dfc;
}
QComboBox::drop-down {
    border: none;
    width: 28px;
}
QComboBox QAbstractItemView {
    background-color: #2a2b4a;
    border: 1px solid #4a4b6e;
    color: #e0e0e8;
    selection-background-color: #7c3aed;
    outline: 0;
}

/* ── Push Buttons ─────────────────────────────────────────── */
QPushButton {
    background-color: #7c3aed;
    color: #ffffff;
    border: none;
    border-radius: 7px;
    padding: 9px 18px;
    font-size: 13px;
    font-weight: 600;
    min-height: 20px;
}
QPushButton:hover {
    background-color: #6d28d9;
}
QPushButton:pressed {
    background-color: #5b21b6;
}
QPushButton:disabled {
    background-color: #3a3b5c;
    color: #6b6c8a;
}

/* Danger button variant */
QPushButton[variant="danger"] {
    background-color: #dc2626;
}
QPushButton[variant="danger"]:hover {
    background-color: #b91c1c;
}

/* Secondary button variant */
QPushButton[variant="secondary"] {
    background-color: #374151;
}
QPushButton[variant="secondary"]:hover {
    background-color: #4b5563;
}

/* Success button variant */
QPushButton[variant="success"] {
    background-color: #059669;
}
QPushButton[variant="success"]:hover {
    background-color: #047857;
}

/* ── Tables ───────────────────────────────────────────────── */
QTableWidget {
    background-color: #222342;
    alternate-background-color: #2a2b4a;
    border: 1px solid #3a3b5c;
    border-radius: 8px;
    gridline-color: #3a3b5c;
    color: #e0e0e8;
    font-size: 12px;
    selection-background-color: #7c3aed44;
    selection-color: #e0e0e8;
}
QTableWidget::item {
    padding: 6px 8px;
    border: none;
}
QTableWidget::item:selected {
    background-color: #7c3aed44;
}
QHeaderView::section {
    background-color: #2d2e50;
    color: #a78bfa;
    border: none;
    border-bottom: 2px solid #7c3aed;
    padding: 8px 6px;
    font-weight: 700;
    font-size: 12px;
}
QHeaderView::section:hover {
    background-color: #3a3b5c;
}

/* ── Scroll Bars ──────────────────────────────────────────── */
QScrollBar:vertical {
    background: #1a1b2e;
    width: 10px;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background: #4a4b6e;
    min-height: 30px;
    border-radius: 5px;
}
QScrollBar::handle:vertical:hover {
    background: #7c3aed;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar:horizontal {
    background: #1a1b2e;
    height: 10px;
    border-radius: 5px;
}
QScrollBar::handle:horizontal {
    background: #4a4b6e;
    min-width: 30px;
    border-radius: 5px;
}
QScrollBar::handle:horizontal:hover {
    background: #7c3aed;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* ── Scroll Area ──────────────────────────────────────────── */
QScrollArea {
    border: none;
    background: transparent;
}

/* ── Splitter ─────────────────────────────────────────────── */
QSplitter::handle {
    background-color: #3a3b5c;
    width: 2px;
}
QSplitter::handle:hover {
    background-color: #7c3aed;
}

/* ── Tab Widget ───────────────────────────────────────────── */
QTabWidget::pane {
    border: 1px solid #3a3b5c;
    border-radius: 8px;
    background-color: #222342;
}
QTabBar::tab {
    background-color: #2a2b4a;
    color: #9b9cb8;
    border: 1px solid #3a3b5c;
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    padding: 8px 16px;
    margin-right: 2px;
    font-weight: 600;
    font-size: 12px;
}
QTabBar::tab:selected {
    background-color: #222342;
    color: #a78bfa;
    border-bottom: 2px solid #7c3aed;
}
QTabBar::tab:hover:!selected {
    background-color: #333460;
    color: #c4c5e0;
}

/* ── Status Bar ───────────────────────────────────────────── */
QStatusBar {
    background-color: #16172b;
    color: #9b9cb8;
    font-size: 12px;
    border-top: 1px solid #3a3b5c;
}

/* ── Message Box ──────────────────────────────────────────── */
QMessageBox {
    background-color: #222342;
}
QMessageBox QLabel {
    color: #e0e0e8;
}

/* ── Tool Tip ─────────────────────────────────────────────── */
QToolTip {
    background-color: #2d2e50;
    color: #e0e0e8;
    border: 1px solid #4a4b6e;
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 12px;
}
"""
