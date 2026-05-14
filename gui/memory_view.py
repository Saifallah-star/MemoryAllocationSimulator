"""
MemoryVisualizationWidget — custom scrollable widget that draws
the memory layout as a vertical stack of colored blocks.

Each block displays its label, address range, and size.
Colors distinguish allocated segments, free holes, and reserved memory.
"""

from typing import List, Dict
from PySide6.QtWidgets import (
    QWidget, QScrollArea, QVBoxLayout, QSizePolicy
)
from PySide6.QtCore import Qt, QRectF, QPropertyAnimation, QEasingCurve

from PySide6.QtGui import (
    QPainter, QColor, QLinearGradient, QFont, QPen, QBrush, QPainterPath
)

from models.memory_block import MemoryBlock, BlockType


# ── Color palette for processes ─────────────────────────────────────────
PROCESS_COLORS: List[tuple] = [
    (124, 58, 237),    # Purple
    (59, 130, 246),    # Blue
    (16, 185, 129),    # Green
    (245, 158, 11),    # Amber
    (239, 68, 68),     # Red
    (236, 72, 153),    # Pink
    (14, 165, 233),    # Sky
    (168, 85, 247),    # Violet
    (251, 146, 60),    # Orange
    (34, 197, 94),     # Emerald
    (99, 102, 241),    # Indigo
    (244, 63, 94),     # Rose
]

HOLE_COLOR = (55, 65, 81)          # Gray-700
RESERVED_COLOR = (30, 31, 50)      # Dark navy
BLOCK_MIN_HEIGHT = 50
PIXELS_PER_KB = 0.6  # Scale factor — adjustable
BLOCK_CORNER_RADIUS = 8
BLOCK_MARGIN = 2
SIDE_PADDING = 14


class MemoryCanvas(QWidget):
    """
    Inner canvas widget that paints the memory blocks.
    Resizes its height dynamically based on total memory size.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.blocks: List[MemoryBlock] = []
        self.total_memory: int = 0
        self._process_color_map: Dict[str, tuple] = {}
        self._color_index = 0
        self.setMinimumWidth(240)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def set_data(self, blocks: List[MemoryBlock], total_memory: int) -> None:
        """Update the blocks to paint and trigger a repaint."""
        self.blocks = blocks
        self.total_memory = total_memory
        self._assign_colors()
        self._recalculate_height()
        self.update()

    def clear_data(self) -> None:
        """Clear the canvas."""
        self.blocks = []
        self.total_memory = 0
        self._process_color_map.clear()
        self._color_index = 0
        self.setFixedHeight(100)
        self.update()

    def _assign_colors(self) -> None:
        """Assign a consistent color to each process."""
        for block in self.blocks:
            if block.block_type == BlockType.ALLOCATED:
                if block.process_name not in self._process_color_map:
                    color = PROCESS_COLORS[
                        self._color_index % len(PROCESS_COLORS)
                    ]
                    self._process_color_map[block.process_name] = color
                    self._color_index += 1

    def _block_height(self, block: MemoryBlock) -> float:
        """Calculate pixel height for a block."""
        h = block.size * PIXELS_PER_KB
        return max(h, BLOCK_MIN_HEIGHT)

    def _recalculate_height(self) -> None:
        """Set widget height based on block sizes."""
        total_h = sum(self._block_height(b) for b in self.blocks)
        total_h += BLOCK_MARGIN * (len(self.blocks) + 1)
        total_h = max(total_h, 100)
        self.setFixedHeight(int(total_h) + 20)

    def paintEvent(self, event):
        """Paint all memory blocks."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if not self.blocks:
            self._draw_empty(painter)
            return

        y = BLOCK_MARGIN + 6
        w = self.width() - SIDE_PADDING * 2

        for block in self.blocks:
            h = self._block_height(block)
            rect = QRectF(SIDE_PADDING, y, w, h)
            self._draw_block(painter, rect, block)
            y += h + BLOCK_MARGIN

        painter.end()

    def _draw_empty(self, painter: QPainter) -> None:
        """Draw placeholder when no data."""
        painter.setPen(QPen(QColor("#6b6c8a")))
        font = QFont("Segoe UI", 13)
        font.setItalic(True)
        painter.setFont(font)
        painter.drawText(
            self.rect(), Qt.AlignCenter,
            "Initialize memory to begin"
        )
        painter.end()

    def _draw_block(self, painter: QPainter, rect: QRectF,
                    block: MemoryBlock) -> None:
        """Draw a single memory block with gradient, label, and addresses."""
        # Determine color
        if block.block_type == BlockType.ALLOCATED:
            base_rgb = self._process_color_map.get(
                block.process_name, PROCESS_COLORS[0]
            )
        elif block.block_type == BlockType.HOLE:
            base_rgb = HOLE_COLOR
        else:
            base_rgb = RESERVED_COLOR

        r, g, b = base_rgb

        # Gradient fill
        gradient = QLinearGradient(rect.topLeft(), rect.bottomLeft())
        gradient.setColorAt(0.0, QColor(r, g, b, 220))
        gradient.setColorAt(1.0, QColor(
            max(r - 30, 0), max(g - 30, 0), max(b - 30, 0), 200
        ))

        # Rounded rect path
        path = QPainterPath()
        path.addRoundedRect(rect, BLOCK_CORNER_RADIUS, BLOCK_CORNER_RADIUS)
        painter.fillPath(path, QBrush(gradient))

        # Border
        border_color = QColor(r, g, b, 120)
        if block.block_type == BlockType.HOLE:
            border_color = QColor(100, 110, 130, 150)
            pen = QPen(border_color, 1.5, Qt.DashLine)
        else:
            pen = QPen(border_color, 1.5)
        painter.setPen(pen)
        painter.drawPath(path)

        # ── Text rendering ──
        text_color = QColor("#ffffff") if block.block_type == BlockType.ALLOCATED \
            else QColor("#c4c5e0")

        # Address labels — left side
        addr_font = QFont("Segoe UI", 9)
        addr_font.setWeight(QFont.Normal)
        painter.setFont(addr_font)
        painter.setPen(QPen(QColor("#9b9cb8")))

        # Start address
        painter.drawText(
            QRectF(rect.x() + 6, rect.y() + 2, rect.width() - 12, 16),
            Qt.AlignLeft | Qt.AlignTop,
            f"{block.start_address}"
        )
        # End address
        painter.drawText(
            QRectF(rect.x() + 6, rect.bottom() - 16, rect.width() - 12, 16),
            Qt.AlignLeft | Qt.AlignBottom,
            f"{block.end_address}"
        )

        # Size label — right side
        painter.drawText(
            QRectF(rect.x(), rect.y() + 2, rect.width() - 8, 16),
            Qt.AlignRight | Qt.AlignTop,
            f"{block.size} KB"
        )

        # Main label — center
        label_font = QFont("Segoe UI", 11)
        label_font.setWeight(QFont.Bold)
        painter.setFont(label_font)
        painter.setPen(QPen(text_color))

        label = block.label
        label_rect = QRectF(
            rect.x() + 8, rect.y() + 8,
            rect.width() - 16, rect.height() - 16
        )
        painter.drawText(label_rect, Qt.AlignCenter, label)


class MemoryVisualizationWidget(QScrollArea):
    """
    Scrollable memory visualization area.
    Wraps the MemoryCanvas in a scroll area for large memory layouts.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.canvas = MemoryCanvas()
        self.setWidget(self.canvas)
        self.setWidgetResizable(False)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setMinimumWidth(280)
        self.setStyleSheet("QScrollArea { border: none; background: #1a1b2e; }")

    def update_visualization(self, blocks: List[MemoryBlock],
                             total_memory: int) -> None:
        """Update the canvas with new memory layout data."""
        self.canvas.set_data(blocks, total_memory)
        # Ensure the canvas width matches the scroll area
        self.canvas.setFixedWidth(max(self.viewport().width() - 4, 260))

    def clear_visualization(self) -> None:
        """Clear the memory visualization."""
        self.canvas.clear_data()

    def resizeEvent(self, event):
        """Keep canvas width in sync with viewport."""
        super().resizeEvent(event)
        if self.canvas:
            self.canvas.setFixedWidth(max(self.viewport().width() - 4, 260))
