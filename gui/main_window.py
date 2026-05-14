"""
MainWindow — The primary application window.
Composes left panel (controls), center panel (visualization),
and right panel (tables) into a 3-column layout.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox,
    QLabel, QLineEdit, QSpinBox, QPushButton, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QSplitter, QTabWidget, QFormLayout, QScrollArea, QSizePolicy,
    QStatusBar, QFileDialog, QApplication
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QIcon, QScreen

from core.memory_manager import MemoryManager, AllocationStrategy
from models.process import Process
from models.segment import Segment
from gui.memory_view import MemoryVisualizationWidget


class MainWindow(QMainWindow):
    """Main application window for the Memory Allocation Simulator."""

    def __init__(self):
        super().__init__()
        self.manager = MemoryManager()
        self._segment_inputs = []  # dynamic segment form rows
        self.setWindowTitle("Memory Allocation Simulator — Segmentation")
        self.setMinimumSize(1200, 700)
        self._center_on_screen()
        self._build_ui()
        self._connect_signals()
        self._refresh_all()

    # ─── Window positioning ─────────────────────────────────────────────

    def _center_on_screen(self):
        screen = QApplication.primaryScreen()
        if screen:
            geo = screen.availableGeometry()
            w = min(1440, int(geo.width() * 0.88))
            h = min(900, int(geo.height() * 0.88))
            x = (geo.width() - w) // 2 + geo.x()
            y = (geo.height() - h) // 2 + geo.y()
            self.setGeometry(x, y, w, h)

    # ─── UI Construction ────────────────────────────────────────────────

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(6)

        splitter = QSplitter(Qt.Horizontal)

        # Left panel (controls)
        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        left_scroll.setMaximumWidth(360)
        left_scroll.setMinimumWidth(280)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(8)
        self._build_memory_init_group(left_layout)
        self._build_hole_group(left_layout)
        self._build_process_group(left_layout)
        self._build_action_group(left_layout)
        self._build_stats_group(left_layout)
        left_layout.addStretch()
        left_scroll.setWidget(left_widget)

        # Center panel (memory visualization)
        self.mem_view = MemoryVisualizationWidget()
        self.mem_view.setMinimumWidth(280)

        # Right panel (tables)
        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setMinimumWidth(360)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setSpacing(8)
        self._build_tables(right_layout)
        right_scroll.setWidget(right_widget)

        splitter.addWidget(left_scroll)
        splitter.addWidget(self.mem_view)
        splitter.addWidget(right_scroll)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 1)

        main_layout.addWidget(splitter)

        # Status bar
        self.statusBar().showMessage("Ready — initialize memory to begin.")

    # ── Memory Init Group ───────────────────────────────────────────────

    def _build_memory_init_group(self, parent_layout):
        grp = QGroupBox("Memory Initialization")
        layout = QFormLayout()
        layout.setSpacing(6)
        self.total_mem_input = QSpinBox()
        self.total_mem_input.setRange(1, 1_000_000)
        self.total_mem_input.setValue(1000)
        self.total_mem_input.setSuffix(" KB")
        layout.addRow("Total Memory:", self.total_mem_input)
        self.btn_init_mem = QPushButton("Initialize Memory")
        layout.addRow(self.btn_init_mem)
        grp.setLayout(layout)
        parent_layout.addWidget(grp)

    # ── Hole Group ──────────────────────────────────────────────────────

    def _build_hole_group(self, parent_layout):
        grp = QGroupBox("Add Free Hole")
        layout = QFormLayout()
        layout.setSpacing(6)
        self.hole_start_input = QSpinBox()
        self.hole_start_input.setRange(0, 999_999)
        self.hole_start_input.setSuffix(" KB")
        layout.addRow("Start Address:", self.hole_start_input)
        self.hole_size_input = QSpinBox()
        self.hole_size_input.setRange(1, 1_000_000)
        self.hole_size_input.setValue(100)
        self.hole_size_input.setSuffix(" KB")
        layout.addRow("Hole Size:", self.hole_size_input)
        self.btn_add_hole = QPushButton("Add Hole")
        self.btn_add_hole.setProperty("variant", "success")
        layout.addRow(self.btn_add_hole)
        grp.setLayout(layout)
        parent_layout.addWidget(grp)

    # ── Process Group ───────────────────────────────────────────────────

    def _build_process_group(self, parent_layout):
        grp = QGroupBox("Add Process")
        layout = QVBoxLayout()
        layout.setSpacing(6)

        form = QFormLayout()
        self.proc_name_input = QLineEdit()
        self.proc_name_input.setPlaceholderText("e.g. P1")
        form.addRow("Process Name:", self.proc_name_input)
        self.num_segments_input = QSpinBox()
        self.num_segments_input.setRange(1, 20)
        self.num_segments_input.setValue(3)
        form.addRow("Num Segments:", self.num_segments_input)
        layout.addLayout(form)

        self.btn_gen_segments = QPushButton("Generate Segment Fields")
        self.btn_gen_segments.setProperty("variant", "secondary")
        layout.addWidget(self.btn_gen_segments)

        # Dynamic segment rows container
        self.segments_container = QVBoxLayout()
        layout.addLayout(self.segments_container)

        self.btn_add_process = QPushButton("Add Process")
        self.btn_add_process.setProperty("variant", "success")
        layout.addWidget(self.btn_add_process)

        grp.setLayout(layout)
        parent_layout.addWidget(grp)

    # ── Action Group ────────────────────────────────────────────────────

    def _build_action_group(self, parent_layout):
        grp = QGroupBox("Allocation / Deallocation")
        layout = QVBoxLayout()
        layout.setSpacing(6)

        form = QFormLayout()
        self.strategy_combo = QComboBox()
        self.strategy_combo.addItems(["First Fit", "Best Fit"])
        form.addRow("Strategy:", self.strategy_combo)

        self.alloc_process_combo = QComboBox()
        self.alloc_process_combo.setPlaceholderText("Select process…")
        form.addRow("Process:", self.alloc_process_combo)
        layout.addLayout(form)

        self.btn_allocate = QPushButton("▶  Allocate Process")
        layout.addWidget(self.btn_allocate)

        self.dealloc_process_combo = QComboBox()
        self.dealloc_process_combo.setPlaceholderText("Select process…")
        layout.addWidget(QLabel("Deallocate:"))
        layout.addWidget(self.dealloc_process_combo)
        self.btn_deallocate = QPushButton("✕  Deallocate Process")
        self.btn_deallocate.setProperty("variant", "danger")
        layout.addWidget(self.btn_deallocate)

        self.btn_reset = QPushButton("⟳  Reset All")
        self.btn_reset.setProperty("variant", "secondary")
        layout.addWidget(self.btn_reset)

        self.btn_export = QPushButton("📷  Export Screenshot")
        self.btn_export.setProperty("variant", "secondary")
        layout.addWidget(self.btn_export)

        grp.setLayout(layout)
        parent_layout.addWidget(grp)

    # ── Stats Group ─────────────────────────────────────────────────────

    def _build_stats_group(self, parent_layout):
        grp = QGroupBox("Statistics")
        layout = QFormLayout()
        layout.setSpacing(4)
        self.lbl_total = QLabel("—")
        self.lbl_used = QLabel("—")
        self.lbl_free = QLabel("—")
        self.lbl_reserved = QLabel("—")
        self.lbl_frag = QLabel("—")
        self.lbl_holes = QLabel("—")
        self.lbl_procs = QLabel("—")
        layout.addRow("Total Memory:", self.lbl_total)
        layout.addRow("Used Memory:", self.lbl_used)
        layout.addRow("Free Memory:", self.lbl_free)
        layout.addRow("Reserved:", self.lbl_reserved)
        layout.addRow("Fragmentation:", self.lbl_frag)
        layout.addRow("Holes:", self.lbl_holes)
        layout.addRow("Processes:", self.lbl_procs)
        grp.setLayout(layout)
        parent_layout.addWidget(grp)

    # ── Tables ──────────────────────────────────────────────────────────

    def _build_tables(self, parent_layout):
        tabs = QTabWidget()

        # Holes table
        self.holes_table = self._make_table(
            ["#", "Start Address", "Size", "End Address"])
        tab1 = QWidget()
        l1 = QVBoxLayout(tab1)
        l1.addWidget(self.holes_table)
        tabs.addTab(tab1, "Free Holes")

        # Allocated partitions table
        self.alloc_table = self._make_table(
            ["Process", "Segment", "Base", "Size", "End"])
        tab2 = QWidget()
        l2 = QVBoxLayout(tab2)
        l2.addWidget(self.alloc_table)
        tabs.addTab(tab2, "Allocated Partitions")

        # Segment tables tab
        self.seg_tables_container = QVBoxLayout()
        tab3_widget = QWidget()
        tab3_widget.setLayout(self.seg_tables_container)
        seg_scroll = QScrollArea()
        seg_scroll.setWidgetResizable(True)
        seg_scroll.setWidget(tab3_widget)
        tabs.addTab(seg_scroll, "Segment Tables")

        parent_layout.addWidget(tabs)

    def _make_table(self, headers):
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.verticalHeader().setVisible(False)
        return table

    # ─── Signal Connections ─────────────────────────────────────────────

    def _connect_signals(self):
        self.btn_init_mem.clicked.connect(self._on_init_memory)
        self.btn_add_hole.clicked.connect(self._on_add_hole)
        self.btn_gen_segments.clicked.connect(self._on_gen_segments)
        self.btn_add_process.clicked.connect(self._on_add_process)
        self.btn_allocate.clicked.connect(self._on_allocate)
        self.btn_deallocate.clicked.connect(self._on_deallocate)
        self.btn_reset.clicked.connect(self._on_reset)
        self.btn_export.clicked.connect(self._on_export)

    # ─── Slot Implementations ───────────────────────────────────────────

    def _on_init_memory(self):
        size = self.total_mem_input.value()
        try:
            self.manager.initialize_memory(size)
            self.statusBar().showMessage(
                f"Memory initialized: {size} KB")
            self._refresh_all()
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", str(e))

    def _on_add_hole(self):
        start = self.hole_start_input.value()
        size = self.hole_size_input.value()
        try:
            self.manager.add_hole(start, size)
            self.statusBar().showMessage(
                f"Hole added: start={start}, size={size}")
            self._refresh_all()
        except (ValueError, RuntimeError) as e:
            QMessageBox.warning(self, "Cannot Add Hole", str(e))

    def _on_gen_segments(self):
        # Clear old segment inputs
        self._clear_segment_inputs()
        n = self.num_segments_input.value()
        for i in range(n):
            row_layout = QHBoxLayout()
            name_edit = QLineEdit()
            name_edit.setPlaceholderText(f"Seg {i+1} name")
            size_spin = QSpinBox()
            size_spin.setRange(1, 999_999)
            size_spin.setValue(50)
            size_spin.setSuffix(" KB")
            row_layout.addWidget(name_edit)
            row_layout.addWidget(size_spin)
            container = QWidget()
            container.setLayout(row_layout)
            self.segments_container.addWidget(container)
            self._segment_inputs.append((name_edit, size_spin, container))

    def _clear_segment_inputs(self):
        for _, _, widget in self._segment_inputs:
            self.segments_container.removeWidget(widget)
            widget.deleteLater()
        self._segment_inputs.clear()

    def _on_add_process(self):
        name = self.proc_name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Invalid", "Process name is required.")
            return
        if not self._segment_inputs:
            QMessageBox.warning(
                self, "Invalid",
                "Generate segment fields first.")
            return

        segments = []
        for name_edit, size_spin, _ in self._segment_inputs:
            seg_name = name_edit.text().strip()
            if not seg_name:
                QMessageBox.warning(
                    self, "Invalid",
                    "All segment names are required.")
                return
            segments.append(Segment(seg_name, size_spin.value()))

        process = Process(name, segments)
        try:
            self.manager.add_process(process)
            self.statusBar().showMessage(
                f"Process '{name}' added ({len(segments)} segments)")
            self._clear_segment_inputs()
            self.proc_name_input.clear()
            self._refresh_all()
        except (ValueError, RuntimeError) as e:
            QMessageBox.warning(self, "Cannot Add Process", str(e))

    def _on_allocate(self):
        proc_name = self.alloc_process_combo.currentData()
        if not proc_name:
            proc_name = self.alloc_process_combo.currentText()
        if not proc_name:
            QMessageBox.warning(
                self, "No Process",
                "Select a process to allocate.")
            return
        strat_text = self.strategy_combo.currentText()
        strategy = (AllocationStrategy.FIRST_FIT
                     if strat_text == "First Fit"
                     else AllocationStrategy.BEST_FIT)
        success, msg = self.manager.allocate_process(proc_name, strategy)
        if success:
            self.statusBar().showMessage(msg)
        else:
            QMessageBox.warning(self, "Allocation Failed", msg)
        self._refresh_all()

    def _on_deallocate(self):
        proc_name = self.dealloc_process_combo.currentData()
        if not proc_name:
            proc_name = self.dealloc_process_combo.currentText()
        if not proc_name:
            QMessageBox.warning(
                self, "No Process",
                "Select a process to deallocate.")
            return
        success, msg = self.manager.deallocate_process(proc_name)
        if success:
            self.statusBar().showMessage(msg)
        else:
            QMessageBox.warning(self, "Deallocation Failed", msg)
        self._refresh_all()

    def _on_reset(self):
        reply = QMessageBox.question(
            self, "Confirm Reset",
            "Reset everything? All data will be lost.",
            QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.manager.reset()
            self.mem_view.clear_visualization()
            self._clear_segment_inputs()
            self._refresh_all()
            self.statusBar().showMessage("Reset complete.")

    def _on_export(self):
        if not self.manager.is_initialized:
            QMessageBox.warning(
                self, "Nothing to export",
                "Initialize memory first.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Export Screenshot", "memory_screenshot.png",
            "PNG Image (*.png)")
        if path:
            pixmap = self.mem_view.grab()
            pixmap.save(path)
            self.statusBar().showMessage(f"Screenshot saved: {path}")

    # ─── Refresh Everything ─────────────────────────────────────────────

    def _refresh_all(self):
        """Re-populate visualization, tables, combos, and stats."""
        self._refresh_visualization()
        self._refresh_holes_table()
        self._refresh_alloc_table()
        self._refresh_segment_tables()
        self._refresh_combos()
        self._refresh_stats()

    def _refresh_visualization(self):
        if self.manager.is_initialized:
            blocks = self.manager.get_memory_layout()
            self.mem_view.update_visualization(
                blocks, self.manager.total_memory)
        else:
            self.mem_view.clear_visualization()

    def _refresh_holes_table(self):
        data = self.manager.get_holes_table_data()
        self.holes_table.setRowCount(len(data))
        for r, d in enumerate(data):
            self.holes_table.setItem(
                r, 0, QTableWidgetItem(str(d["hole_number"])))
            self.holes_table.setItem(
                r, 1, QTableWidgetItem(str(d["start_address"])))
            self.holes_table.setItem(
                r, 2, QTableWidgetItem(str(d["size"])))
            self.holes_table.setItem(
                r, 3, QTableWidgetItem(str(d["end_address"])))

    def _refresh_alloc_table(self):
        data = self.manager.get_allocated_partitions_data()
        self.alloc_table.setRowCount(len(data))
        for r, d in enumerate(data):
            self.alloc_table.setItem(
                r, 0, QTableWidgetItem(d["process_name"]))
            self.alloc_table.setItem(
                r, 1, QTableWidgetItem(d["segment_name"]))
            self.alloc_table.setItem(
                r, 2, QTableWidgetItem(str(d["base_address"])))
            self.alloc_table.setItem(
                r, 3, QTableWidgetItem(str(d["size"])))
            self.alloc_table.setItem(
                r, 4, QTableWidgetItem(str(d["end_address"])))

    def _refresh_segment_tables(self):
        # Clear previous
        while self.seg_tables_container.count():
            item = self.seg_tables_container.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        all_tables = self.manager.get_all_segment_tables()
        if not all_tables:
            lbl = QLabel("No processes added yet.")
            lbl.setStyleSheet("color:#6b6c8a; font-style:italic; padding:12px;")
            self.seg_tables_container.addWidget(lbl)
            return

        for proc_name, rows in all_tables.items():
            grp = QGroupBox(f"Process: {proc_name}")
            grp_layout = QVBoxLayout()
            tbl = self._make_table(
                ["Segment", "Base Address", "Limit", "Status"])
            tbl.setRowCount(len(rows))
            for r, d in enumerate(rows):
                tbl.setItem(r, 0, QTableWidgetItem(d["segment_name"]))
                tbl.setItem(
                    r, 1, QTableWidgetItem(str(d["base_address"])))
                tbl.setItem(r, 2, QTableWidgetItem(str(d["limit"])))
                status = "Allocated" if d["allocated"] else "Pending"
                tbl.setItem(r, 3, QTableWidgetItem(status))
            tbl.setMaximumHeight(40 + len(rows) * 32)
            grp_layout.addWidget(tbl)
            grp.setLayout(grp_layout)
            self.seg_tables_container.addWidget(grp)

        self.seg_tables_container.addStretch()

    def _refresh_combos(self):
        # Unallocated processes for allocation combo
        self.alloc_process_combo.clear()
        for name, proc in self.manager.processes.items():
            if not proc.is_allocated:
                self.alloc_process_combo.addItem(name, name)

        # All registered processes for deallocation combo
        self.dealloc_process_combo.clear()
        for name, proc in self.manager.processes.items():
            state = "allocated" if proc.is_allocated else "free"
            self.dealloc_process_combo.addItem(
                f"{name} ({state})", name)

    def _refresh_stats(self):
        s = self.manager.get_statistics()
        self.lbl_total.setText(f"{s['total']} KB")
        self.lbl_used.setText(f"{s['used']} KB")
        self.lbl_free.setText(f"{s['free']} KB")
        self.lbl_reserved.setText(f"{s['reserved']} KB")
        self.lbl_frag.setText(f"{s['fragmentation']}%")
        self.lbl_holes.setText(str(s['num_holes']))
        self.lbl_procs.setText(str(s['num_processes']))
