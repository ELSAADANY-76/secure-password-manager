from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar

class StrengthBar(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self.label = QLabel("Strength: —")
        self.label.setStyleSheet("font-size: 12px; color: gray;")

        self.bar = QProgressBar()
        self.bar.setFixedHeight(8)
        self.bar.setMaximum(100)
        self.bar.setValue(0)
        self.bar.setTextVisible(False)

        layout.addWidget(self.label)
        layout.addWidget(self.bar)
        self.setLayout(layout)

    def update_strength(self, strength: str):
        if strength == 'Weak':
            self.bar.setValue(33)
            self.bar.setStyleSheet(
                "QProgressBar::chunk { background-color: #ef4444; "
                "border-radius: 4px; }"
            )
            self.label.setText("Strength: Weak")
        elif strength == 'Medium':
            self.bar.setValue(66)
            self.bar.setStyleSheet(
                "QProgressBar::chunk { background-color: #f59e0b; "
                "border-radius: 4px; }"
            )
            self.label.setText("Strength: Medium")
        else:
            self.bar.setValue(100)
            self.bar.setStyleSheet(
                "QProgressBar::chunk { background-color: #22c55e; "
                "border-radius: 4px; }"
            )
            self.label.setText("Strength: Strong")