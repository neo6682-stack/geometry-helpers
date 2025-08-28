#!/usr/bin/env python3
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QLabel, QPushButton,
    QComboBox, QFormLayout, QVBoxLayout, QMessageBox
)
from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import Qt

def rectangle_area(length: float, width: float) -> float:
    if length <= 0 or width <= 0:
        raise ValueError("Length and width must be positive numbers.")
    return length * width

class AreaCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Area Calculator")

        # Inputs
        self.length_input = QLineEdit()
        self.width_input  = QLineEdit()

        # Only allow numbers (with decimals)
        validator = QDoubleValidator(0.0, 1e12, 6)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.length_input.setValidator(validator)
        self.width_input.setValidator(validator)

        # Units
        self.unit_combo = QComboBox()
        self.unit_combo.setEditable(True)
        self.unit_combo.addItems(["", "m", "cm", "mm", "in", "ft"])

        # Output
        self.result_label = QLabel("—")
        self.result_label.setAlignment(Qt.AlignLeft)

        # Buttons
        self.calc_btn = QPushButton("Calculate")
        self.clear_btn = QPushButton("Clear")

        # Layout
        form = QFormLayout()
        form.addRow("Length (> 0):", self.length_input)
        form.addRow("Width  (> 0):", self.width_input)
        form.addRow("Unit (optional):", self.unit_combo)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.calc_btn)
        layout.addWidget(self.clear_btn)
        layout.addWidget(QLabel("Area:"))
        layout.addWidget(self.result_label)
        layout.addStretch(1)
        self.setLayout(layout)

        # Events
        self.calc_btn.clicked.connect(self.calculate)
        self.clear_btn.clicked.connect(self.clear_fields)
        self.length_input.returnPressed.connect(self.calculate)
        self.width_input.returnPressed.connect(self.calculate)

    def _read_float(self, line_edit: QLineEdit, name: str) -> float:
        text = line_edit.text().strip()
        if not text:
            raise ValueError(f"{name} is required.")
        try:
            value = float(text)
        except ValueError:
            raise ValueError(f"{name} must be a valid number.")
        if value <= 0:
            raise ValueError(f"{name} must be > 0.")
        return value

    def calculate(self):
        try:
            length = self._read_float(self.length_input, "Length")
            width  = self._read_float(self.width_input,  "Width")
            area   = rectangle_area(length, width)
        except ValueError as e:
            QMessageBox.critical(self, "Input Error", str(e))
            return

        unit = self.unit_combo.currentText().strip()
        self.result_label.setText(f"{area} {unit}²" if unit else str(area))

    def clear_fields(self):
        self.length_input.clear()
        self.width_input.clear()
        self.result_label.setText("—")
        self.length_input.setFocus()

def main():
    app = QApplication(sys.argv)
    w = AreaCalculator()
    w.resize(360, 240)
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
